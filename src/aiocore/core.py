from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from aiogram.fsm.storage.memory import MemoryStorage, MemoryStorageRecord

from typing import Callable, Awaitable, Dict, Any

from src.aiocore import Database
from src.aiocore import Config
from src.aiocore import Logger
from src.aiocore import Content
from src.aiocore import Keyboard
from src.aiocore import FSMStorage

# Database services
from src.aiocore.services.database import UserRepository


class CoreServices:
    def __init__(
            self,
            user_repository: UserRepository,
            content: Content,
            keyboard: Keyboard,
            fsm_storage: FSMStorage,
            logger: Logger
    ):
        """
        The core object that stores database services, injectors
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
        self.logger = logger


class CoreMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.message.from_user.id

        # Base objects
        database = Database()
        config = Config()
        logger = Logger()

        # Core services
        user_repository = UserRepository(database=database)
        content = Content(user_repository=user_repository, config=config, user_id=user_id)
        keyboard = Keyboard(user_repository=user_repository, config=config, user_id=user_id)
        fsm_storage = FSMStorage(user_repository=user_repository)

        data["core"] = CoreServices(
            user_repository=user_repository,
            content=content,
            keyboard=keyboard,
            fsm_storage=fsm_storage,
            logger=logger
        )

        await handler(event, data)

        # Save FSMContext
        user_state: MemoryStorage = data["fsm_storage"]
        memory_storage: MemoryStorageRecord = list(user_state.storage.values())[0]
        fsm_storage.save_user_state(user_id, memory_storage.state, memory_storage.data)
