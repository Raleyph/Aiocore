from typing import Optional
from aiogram import types
from src.aiocore import CoreServices

from src.aiocore.services.injectors import (
    MainMenuMessageInjector
)

from src.aiocore.services.injectors import (
    MainMenuKeyboardInjector
)

from src.content.messages import *
from src.content.keyboards import *


class RepeatedAnswers:
    """
    The BaseAnswers class contains static methods that return answers that are repeatedly repeated
    """

    @staticmethod
    async def no_option_answer(
            core: CoreServices,
            message: types.Message,
            answer_keyboard: dict[dict, list],
            row_size: int = 2,
            page: Optional[int] = None
    ):
        return await message.answer(
            text=core.content.get_message_text(no_option_message),
            reply_markup=core.keyboard.get_keyboard(
                keyboard=answer_keyboard,
                is_inline=False,
                row_size=row_size,
                page=page
            ),
            parse_mode="html"
        )

    @staticmethod
    async def main_menu_answer(
            core: CoreServices,
            message: types.Message,
            row_size: int = 2,
            page: Optional[int] = None
    ):
        return await message.answer(
            text=core.content.get_message_text(
                main_menu_message,
                injector=MainMenuMessageInjector()
            ),
            reply_markup=core.keyboard.get_keyboard(
                keyboard=main_keyboard,
                is_inline=False,
                row_size=row_size,
                page=page,
                injector=MainMenuKeyboardInjector()
            ),
            parse_mode="html"
        )
