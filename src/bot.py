from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.aiocore import Config
from src.aiocore import Database
from src.aiocore import Content
from src.aiocore import Keyboard

from src.aiocore import UserStorage

from src.aiocore.middlewares.state_storage import StateStorageMiddleware

import asyncio

# base objects
config = Config()
database = Database()

# services
users = UserStorage(database)
content = Content(users, config)
keyboard = Keyboard(content)

# bot objects
bot = Bot(config.get_parameter("Default", "bot_token"))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    from handlers import start_handler, menu_handler
    from src.aiocore import FSMReset

    dp.include_router(start_handler.router)
    dp.include_router(menu_handler.router)

    dp.update.middleware.register(StateStorageMiddleware(users))

    await FSMReset(users).reset_user_states(bot, dp.fsm.storage)

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
