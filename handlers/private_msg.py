from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.database import async_session
from database.orm_queries import check_for_subs, get_schedule, get_subs
from keyboards.group_kb import group_dict
from keyboards.inline import create_buttons_inline

private_router = Router()

BASE_KB = create_buttons_inline(
    buttons={
        'Расписание группы': 'group_dashboard',
        'Расписание всех групп на сайте':
            'https://spb-kit.ru/studentam/raspisanie_zanyatiy_zameny/',
    },
    sizes=(1, 1)
)

COURSE_KB = create_buttons_inline(
    buttons={
        '1 курс': 'course_1',
        '2 курс': 'course_2',
        '3 курс': 'course_3',
        '4 курс': 'course_4',
        'Назад': 'home'
    },
    sizes=(2, 2)
)


class BotMessage(StatesGroup):
    message_id = State()
    chat_id = State()


@private_router.message(CommandStart())
async def hello(message: types.Message, bot: Bot, state: FSMContext):
    bot_message = await message.answer(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇',
        reply_markup=BASE_KB
    )
    await state.set_state(BotMessage.message_id)
    await state.update_data(message_id=bot_message.message_id)
    await state.set_state(BotMessage.chat_id)
    await state.update_data(chat_id=bot_message.chat.id)


@private_router.message(Command('about'))
async def about(message: types.Message, bot: Bot):
    await message.answer(
        'Бот показывает расписание и замены.\n'
        'github репозиторий - https://github.com/Aserold/kit_goodbot.\n'
        'Прошу сообщать о проблемах в лс @aserold'
    )


@private_router.callback_query(F.data == 'home')
async def home(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    message_data = await state.get_data()
    await bot.edit_message_text(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇',
        chat_id=message_data['chat_id'],
        message_id=message_data['message_id'],
        reply_markup=BASE_KB,
    )


@private_router.callback_query(F.data == 'group_dashboard')
async def group_dashboard(
        callback: types.CallbackQuery, bot: Bot, state: FSMContext
):
    message_data = await state.get_data()
    await bot.edit_message_text(
        'Пожалуйста выберите ваш курс👇',
        chat_id=message_data['chat_id'],
        message_id=message_data['message_id'],
        reply_markup=COURSE_KB
    )


@private_router.callback_query(F.data.startswith('course_'))
async def get_course(
        callback: types.CallbackQuery, bot: Bot, state: FSMContext
):
    message_data = await state.get_data()
    await bot.edit_message_text(
        'Пожалуйста выберите ваш группу👇',
        chat_id=message_data['chat_id'],
        message_id=message_data['message_id'],
        reply_markup=group_dict[int(callback.data.split('_')[-1])]
        )


@private_router.callback_query(F.data.startswith('groupnum_'))
async def get_week_schedule(
        callback: types.CallbackQuery,
        bot: Bot,
        state: FSMContext,
        session=async_session
):
    message_data = await state.get_data()
    group_num = int(callback.data.split('_')[-1])
    schedule: list[tuple, ...] = await get_schedule(session, group_num)
    current_weekday = None
    response_message = ''

    for lesson in schedule:
        weekday = lesson[0]
        start_time = lesson[1].strftime('%H:%M')
        subject = lesson[2]
        if not current_weekday or current_weekday != weekday:
            current_weekday = weekday
            response_message += (f'<b>{weekday}</b>\n'
                                 f'<i>{start_time}: </i>{subject}\n')
        elif current_weekday == weekday:
            response_message += f'<i>{start_time}: </i>{subject}\n'
    if await check_for_subs(session, group_num):
        subs = await get_subs(session, group_num)
        day = subs[0]['day']
        date = subs[1]['date']
        response_message += (f'\n<strong>ЗАМЕНЫ НА '
                             f'{date.strftime('%d.%m.%y')} - '
                             f'{day}</strong>\n\n')
        for sub in subs[2:]:
            lecture_num = sub['lecture_number']
            subject = sub['subject']
            substitute_teacher = sub['substitute_teacher']
            new_subject = sub['new_subject']
            classroom = sub['classroom']
            if subject and new_subject:
                response_message +=\
                    (f'{lecture_num} лекция зам. предмет - {subject}\n'
                     f'преподаёт - {substitute_teacher} '
                     f'нов. предмет - {new_subject} {classroom}\n\n')
            elif (not subject) and new_subject:
                response_message += \
                    (f'{lecture_num} лекция - НОВАЯ ПАРА\n'
                     f'Преподаёт - {substitute_teacher} '
                     f'Предмет - {new_subject} {classroom}\n\n')
            elif subject and (not new_subject):
                response_message += \
                    (f'{lecture_num} лекция зам. предмет - {subject}\n'
                     f'ПАРА ОТМЕНЕНА ИЛИ ПЕРЕНЕСЕНА\n\n')

    await bot.edit_message_text(response_message,
                                chat_id=message_data['chat_id'],
                                message_id=message_data['message_id'],
                                reply_markup=create_buttons_inline(
                                    buttons={
                                        'Назад к курсам': 'group_dashboard',
                                        'В начало': 'home'
                                    },
                                    sizes=(1, 1)
                                ))
