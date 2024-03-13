import asyncio
import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from common.commands import private
from config import TOKEN
from handlers.private_msg import private_router

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
redis = Redis(port=6378)
storage = RedisStorage(
    redis=redis,
    data_ttl=datetime.timedelta(days=183),
    state_ttl=datetime.timedelta(days=183),
)
dp = Dispatcher(storage=storage)

dp.include_router(private_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=private, scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
