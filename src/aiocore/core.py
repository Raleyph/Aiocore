from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any

from src.aiocore import Database
from src.aiocore import Config
from src.aiocore import Content
from src.aiocore import Keyboard
from src.aiocore import FSMStorage

from src.aiocore.services.database import UserRepository


class CoreServices:
    def __init__(
            self,
            user_repository: UserRepository,
            content: Content,
            keyboard: Keyboard,
            fsm_storage: FSMStorage
    ):
        """
        The core object that stores database services, content
        manager, keyboard manager and FSM storage.

        :param user_repository:
        :param content:
        :param keyboard:
        :param fsm_storage:
        """
        self.user_repository = user_repository
        self.content = content
        self.keyboard = keyboard
        self.fsm_storage = fsm_storage


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

        data["core"] = CoreServices(
            user_repository=user_repository,
            content=content,
            keyboard=keyboard,
            fsm_storage=fsm_storage
        )

        return await handler(event, data)
