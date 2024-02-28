from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import create_buttons_inline
from keyboards.group_kb import group_dict
from database.orm_queries import get_schedule
from database.database import async_session

private_router = Router()

BASE_KB = create_buttons_inline(
    buttons={
        'Расписание группы': 'group_dashboard',
        'Расписание всех групп на сайте': 'https://spb-kit.ru/studentam/raspisanie_zanyatiy_zameny/',
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
    initial_message = State()


@private_router.message(CommandStart())
async def hello(message: types.Message, bot: Bot, state: FSMContext):
    first_message = await message.answer(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇', reply_markup=BASE_KB
    )
    await state.update_data(initial_message=first_message)
    message_data: types.Message = (await state.get_data())['initial_message']


@private_router.callback_query(F.data == 'home')
async def home(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    message_data: types.Message = (await state.get_data())['initial_message']
    await bot.edit_message_text(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇',
        chat_id=message_data.chat.id,
        message_id=message_data.message_id,
        reply_markup=BASE_KB,
    )


@private_router.callback_query(F.data == 'group_dashboard')
async def group_dashboard(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    message_data: types.Message = (await state.get_data())['initial_message']
    await bot.edit_message_text('Пожалуйста выберите ваш курс👇',
                                chat_id=message_data.chat.id,
                                message_id=message_data.message_id,
                                reply_markup=COURSE_KB)


@private_router.callback_query(F.data.startswith('course_'))
async def get_course(callback: types.CallbackQuery, bot: Bot, state: FSMContext):
    message_data: types.Message = (await state.get_data())['initial_message']
    await bot.edit_message_text('Пожалуйста выберите ваш группу👇',
                                chat_id=message_data.chat.id,
                                message_id=message_data.message_id,
                                reply_markup=group_dict[int(callback.data.split('_')[-1])]
                                )


@private_router.callback_query(F.data.startswith('groupnum_'))
async def get_week_schedule(callback: types.CallbackQuery, bot: Bot, state: FSMContext, session=async_session):
    message_data: types.Message = (await state.get_data())['initial_message']
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
            response_message += f'<b>{weekday}</b>\n<i>{start_time}: </i>{subject}\n'
        elif current_weekday == weekday:
            response_message += f'<i>{start_time}: </i>{subject}\n'

    await bot.edit_message_text(response_message,
                                chat_id=message_data.chat.id,
                                message_id=message_data.message_id,
                                reply_markup=create_buttons_inline(
                                    buttons={
                                        'Назад к курсам': 'group_dashboard',
                                        'В начало': 'home'
                                    },
                                    sizes=(1, 1)
                                ))
