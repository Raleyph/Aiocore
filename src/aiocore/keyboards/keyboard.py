from typing import Optional

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

from src.aiocore import Content
from src.aiocore.keyboards.markup import KeyboardMarkup


class Keyboard:
    def __init__(self, content: Content):
        """ Initialize keyboard object """
        self.__markup = KeyboardMarkup(content)

    def get_reply_keyboard(
            self,
            keyboard_name: str,
            user_id: int,
            row_size: int = 2,
            page: Optional[int] = None
    ) -> ReplyKeyboardMarkup:
        """
        Return reply keyboard markup object

        :param keyboard_name:
        :param user_id:
        :param row_size:
        :param page:
        :return:
        """
        kb = ReplyKeyboardBuilder()
        keyboard_markup = self.__markup.get_reply_keyboard_markup(keyboard_name, user_id, row_size, page)

        for row in keyboard_markup:
            kb.row(*row)

        return kb.as_markup(resize_keyboard=True)

    def get_inline_keyboard(
            self,
            keyboard_name: str,
            user_id: int,
            row_size: int = 2
    ) -> InlineKeyboardMarkup:
        """
        Return inline keyboard markup object

        :param keyboard_name:
        :param user_id:
        :param row_size:
        :return:
        """
        kb = InlineKeyboardBuilder()
        keyboard_buttons = self.__markup.get_inline_keyboard_markup(keyboard_name, user_id, row_size)

        for row in keyboard_buttons:
            kb.row(*row)

        return kb.as_markup()

    @staticmethod
    def get_button_name(
            keyboard: dict,
            button_text: str
    ):
        """
        Return button name

        :param keyboard:
        :param button_text:
        :return:
        """
        return dict(zip(keyboard.values(), keyboard.keys())).get(button_text)
