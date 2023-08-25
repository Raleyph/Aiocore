from typing import Optional

from aiogram import types

from src.aiocore import Content
from src.aiocore import Keyboard


class BaseAnswers:
    @staticmethod
    async def no_option_answer(
            content: Content,
            keyboard: Keyboard,
            message: types.Message,
            answer_keyboard: str,
            keyboard_row_size: int = 2,
            keyboard_page: Optional[int] = None
    ):
        return await message.answer(text=content.get_message_text("no_option", message.from_user.id),
                                    reply_markup=keyboard.get_reply_keyboard(answer_keyboard, message.from_user.id,
                                                                             keyboard_row_size, keyboard_page),
                                    parse_mode="html")
