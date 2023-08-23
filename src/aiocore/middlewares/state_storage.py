from aiogram import BaseMiddleware
from aiogram.types import Message

from typing import Callable, Awaitable, Dict, Any

from src.aiocore import UserStorage
from src.aiocore import FSMReset


class StateStorageMiddleware(BaseMiddleware):
    def __init__(self, users: UserStorage):
        self.users = users

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        data["state_storage"] = FSMReset(self.users)
        return await handler(event, data)
