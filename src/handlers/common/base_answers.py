from typing import Optional

from aiogram import types

from src.bot import content, keyboard


class BaseAnswers:
    @staticmethod
    async def no_option_answer(
            message: types.Message,
            answer_keyboard: str,
            user_id: Optional[int] = None
    ):
        return await message.answer(text=content.get_message_text("no_option", user_id),
                                    reply_markup=keyboard.get_reply_keyboard(answer_keyboard, user_id),
                                    parse_mode="html")
