from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.aiocore import ConfigReader

from handlers import main_handler

import asyncio

cfg = ConfigReader()

bot = Bot(cfg.get_parameter("Default", "bot_token"))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(main_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def close():
    await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except:
        loop.run_until_complete(close())
