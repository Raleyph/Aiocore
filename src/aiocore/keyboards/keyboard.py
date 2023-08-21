from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

from src.aiocore.keyboards.markup import MarkupManager

markup = MarkupManager()


class Keyboard:
    def __init__(self):
        """ Initialize keyboard object """
        pass

    @staticmethod
    def get_reply_keyboard(
            keyboard_name: str,
            user_id: int,
            row_size: int = 2
    ) -> ReplyKeyboardMarkup:
        """
        Return reply keyboard markup object

        :param keyboard_name:
        :param user_id:
        :param row_size:
        :return:
        """
        kb = ReplyKeyboardBuilder()
        keyboard_markup = markup.get_reply_keyboard_markup(keyboard_name, user_id, row_size)

        for row in keyboard_markup:
            kb.row(*row)

        return kb.as_markup(resize_keyboard=True)

    @staticmethod
    def get_inline_keyboard(
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
        keyboard_buttons = markup.get_inline_keyboard_markup(keyboard_name, user_id, row_size)

        for row in keyboard_buttons:
            kb.row(*row)

        return kb.as_markup()
