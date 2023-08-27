from typing import Optional

from aiogram import types

from src.aiocore import Content
from src.aiocore import Keyboard

from src.aiocore.services.content import (
    MainMenuMessageInjector
)

from src.aiocore.services.content import (
    MainMenuKeyboardInjector
)

from src.content.messages import *
from src.content.keyboards import *


class BaseAnswers:
    """
    The BaseAnswers class contains static methods that return answers that are repeatedly repeated
    """

    @staticmethod
    async def no_option_answer(
            content: Content,
            keyboard: Keyboard,
            message: types.Message,
            answer_keyboard: dict[dict, list],
            row_size: int = 2,
            page: Optional[int] = None
    ):
        return await message.answer(text=content.get_message_text(no_option_message),
                                    reply_markup=keyboard.get_keyboard(
                                        keyboard=answer_keyboard,
                                        is_inline=False,
                                        row_size=row_size,
                                        page=page
                                    ),
                                    parse_mode="html")

    @staticmethod
    async def main_menu_answer(
            content: Content,
            keyboard: Keyboard,
            message: types.Message,
            row_size: int = 2,
            page: Optional[int] = None
    ):
        return await message.answer(text=content.get_message_text(
                                        main_menu_message,
                                        injector=MainMenuMessageInjector()),
                                    reply_markup=keyboard.get_keyboard(
                                        keyboard=main_keyboard,
                                        is_inline=False,
                                        row_size=row_size,
                                        page=page,
                                        injector=MainMenuKeyboardInjector()
                                    ),
                                    parse_mode="html")
