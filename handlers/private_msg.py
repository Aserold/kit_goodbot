from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.inline import create_buttons_inline
from keyboards.group_kb import group_dict

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


class BotMessage:
    """
    Класс для хранения первого сообщения Бота.

    Attributes:
        initial_message (types.Message): Первое сообщение пользователя.
    """

    initial_message: types.Message = None


@private_router.message(CommandStart())
async def hello(message: types.Message, bot: Bot):
    if BotMessage.initial_message is None:
        BotMessage.initial_message = await message.answer(
            'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇', reply_markup=BASE_KB
        )


@private_router.callback_query(F.data == 'home')
async def home(callback: types.CallbackQuery, bot: Bot):
    await bot.edit_message_text(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇',
        chat_id=BotMessage.initial_message.chat.id,
        message_id=BotMessage.initial_message.message_id,
        reply_markup=BASE_KB,
    )


class AddUserGroup(StatesGroup):
    user_id = State()
    user_course = State()
    user_group = State()


@private_router.callback_query(F.data == 'group_dashboard')
async def group_dashboard(callback: types.CallbackQuery, bot: Bot):
    if BotMessage.initial_message:
        await bot.edit_message_text('Пожалуйста выберите ваш курс👇',
                                    chat_id=BotMessage.initial_message.chat.id,
                                    message_id=BotMessage.initial_message.message_id,
                                    reply_markup=COURSE_KB)


@private_router.callback_query(F.data.startswith('course_'))
async def get_course(callback: types.CallbackQuery, bot: Bot):
    if BotMessage.initial_message:
        await bot.edit_message_text('Пожалуйста выберите ваш группу👇',
                                    chat_id=BotMessage.initial_message.chat.id,
                                    message_id=BotMessage.initial_message.message_id,
                                    reply_markup=group_dict[int(callback.data.split('_')[-1])]
                                    )
