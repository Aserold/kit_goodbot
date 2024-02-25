from aiogram import Router, types, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup

from keyboards.inline import create_buttons_inline

private_router = Router()

BASE_KB = create_buttons_inline(
    buttons={
        'Расписание группы': 'group_dashboard',
        'Расписание всех групп на сайте': 'https://spb-kit.ru/studentam/raspisanie_zanyatiy_zameny/',
    },
    sizes=(1, 1)
)


class BotMessage:
    initial_message: types.Message = None


@private_router.message(CommandStart())
async def hello(message: types.Message):
    BotMessage.initial_message = await message.answer(
        'Здравствуйте! Пожалуйста нажмите на кнопку ниже👇', reply_markup=BASE_KB
    )


class AddUserGroup(StatesGroup):
    pass


@private_router.callback_query(F.data == 'group_dashboard')
async def group_dashboard(callback: types.CallbackQuery, bot: Bot):
    if BotMessage.initial_message:
        await bot.edit_message_text('Worked', chat_id=BotMessage.initial_message.chat.id,
                                    message_id=BotMessage.initial_message.message_id)
