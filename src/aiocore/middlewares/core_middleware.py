from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any

from src.aiocore import Database, Config
from src.aiocore import Content, Keyboard
from src.aiocore import UserRepository
from src.aiocore import FSMStorage
from src.aiocore import CoreServices


class CoreMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        __database = Database()
        __config = Config()

        user_repository = UserRepository(database=__database)
        content = Content(user_repository=user_repository, config=__config)
        keyboard = Keyboard(content=content)
        fsm_storage = FSMStorage(user_repository=user_repository)

        data["core"] = CoreServices(user_repository, content, keyboard, fsm_storage)
        return await handler(event, data)
