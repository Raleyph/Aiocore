from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.aiocore import Config

import asyncio

config = Config()

bot = Bot(config.get_parameter("Default", "bot_token"))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    """
    Called during bot startup

    :return:
    """
    from src.aiocore import Database
    from src.aiocore import FSMStorage
    from src.aiocore.services.database import UserRepository

    from src.aiocore.core import CoreMiddleware

    from handlers import start_handler, menu_handler, admin_handler

    # routers
    dp.include_router(start_handler.router)
    dp.include_router(menu_handler.router)
    dp.include_router(admin_handler.router)

    # middlewares
    dp.update.middleware.register(CoreMiddleware())

    # reset users state
    fsm_reset = FSMStorage(UserRepository(database=Database()))
    await fsm_reset.reset_user_states(bot=bot, storage=dp.fsm.storage)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def close():
    """
    Called during bot shutdown

    :return:
    """
    await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(close())
    except Exception as exception:
        print(exception)
