from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.base import BaseStorage

from aiogram import Bot

from src.aiocore.services.database import UserRepository

import json


class FSMData:
    def __init__(
            self,
            context: FSMContext,
            state: str,
            state_data: dict
    ):
        """
        Service for save the user state and state data after bot restart

        :param context:
        :param state:
        :param state_data:
        """
        self.context = context
        self.state = state
        self.state_data = state_data


class FSMStorage:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def __get_user_states(
            self,
            bot: Bot,
            storage: BaseStorage
    ) -> list[FSMData]:
        """
        Get user data from database and return list of
        FSMData objects (contains FSMContext, State and StateData)

        :param bot:
        :param storage:
        :return:
        """
        users = self.__user_repository.get_all_users(["user_id", "chat_id", "state", "state_data"])
        user_states = []

        for user in users:
            user_id = user[0]
            chat_id = user[1]
            state = user[2]
            state_data = json.loads(user[3].replace("\'", "\""))

            key = StorageKey(bot.id, chat_id, user_id)
            context = FSMContext(bot, storage, key)

            user_states.append(FSMData(context, state, state_data))

        return user_states

    async def reset_user_states(
            self,
            bot: Bot,
            storage: BaseStorage
    ):
        """
        Reset user states after bot restart

        :param bot:
        :param storage:
        :return:
        """
        from src.aiocore.fsm import states

        users_fsm: list[FSMData] = self.__get_user_states(bot, storage)

        for fsm_data in users_fsm:
            state_name = fsm_data.state.split(":")
            state_class = getattr(states, state_name[0])
            state_object = getattr(state_class, state_name[1])

            state_data = fsm_data.state_data

            await fsm_data.context.set_state(state_object)
            await fsm_data.context.update_data(**state_data)

    def save_user_state(
            self,
            user_id: int,
            state: str,
            state_data: dict
    ):
        """
        Save state of current user (using middleware)

        :param user_id:
        :param state:
        :param state_data:
        :return:
        """
        self.__user_repository.save_user_state(user_id, state, state_data.__str__())
