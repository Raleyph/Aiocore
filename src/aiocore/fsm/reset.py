from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage, StorageKey

from aiogram import Bot

from src.aiocore import UserRepository


class FSMReset:
    def __init__(self, users: UserRepository):
        self.users = users

    def get_user_states(self, bot: Bot, storage: BaseStorage) -> dict:
        users = self.users.get_all_users(["user_id", "chat_id", "state", "state_data"])
        user_states = {}

        for user in users:
            user_id = user[0]
            chat_id = user[1]

            key = StorageKey(bot.id, chat_id, user_id)
            user_states[user_id] = FSMContext(bot, storage, key)

        return user_states

    def set_current_state(self, users: dict):
        pass
