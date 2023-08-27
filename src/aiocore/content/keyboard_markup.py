from aiogram.types import KeyboardButton, InlineKeyboardButton

MAX_REPLY_ROW_SIZE = 4
MAX_INLINE_ROW_SIZE = 2
BUTTON_TEXT_LENGTH_BORDER = 15


class KeyboardMarkup:
    def __init__(self, keyboard_buttons: dict[str, str]):
        """ Initialize markup manager """
        self.keyboard_buttons = keyboard_buttons

    def get_reply_keyboard_markup(
            self,
            row_size: int = 2,
    ) -> list:
        """
        Return sorted reply keyboard markup

        :param row_size:
        :return:
        """
        if row_size > MAX_REPLY_ROW_SIZE or row_size < 0:
            raise RowSizeError(row_size)

        keyboard_markup = []

        def add_new_row(new_button_text: str):
            keyboard_markup.append([KeyboardButton(text=new_button_text)])

        for button_text in self.keyboard_buttons.values():
            if (
                len(button_text) > BUTTON_TEXT_LENGTH_BORDER
                or not keyboard_markup
            ):
                add_new_row(button_text)
                continue

            for row in keyboard_markup:
                last_row = keyboard_markup[len(keyboard_markup) - 1]

                if row is last_row:
                    if (
                        len("".join([last_row_button_text.text
                                     for last_row_button_text in last_row])) <= BUTTON_TEXT_LENGTH_BORDER
                        and len(row) < row_size
                    ):
                        row.append(KeyboardButton(text=button_text))
                    else:
                        add_new_row(button_text)

                    break

        return keyboard_markup

    def get_inline_keyboard_markup(
            self,
            row_size: int = 2
    ) -> list:
        """
        Return sorted inline keyboard markup

        :param row_size:
        :return:
        """
        if row_size > MAX_INLINE_ROW_SIZE or row_size < 0:
            raise RowSizeError(row_size)

        keyboard_markup = []

        def add_new_row(new_button_text: str, new_button_callback_data: str):
            keyboard_markup.append([InlineKeyboardButton(text=new_button_text,
                                                         callback_data=new_button_callback_data)])

        for button_name, button_text in self.keyboard_buttons.items():
            if (
                len(button_text) > BUTTON_TEXT_LENGTH_BORDER
                or not keyboard_markup
            ):
                add_new_row(button_text, button_name)
                continue

            for row in keyboard_markup:
                last_row = keyboard_markup[len(keyboard_markup) - 1]

                if row is last_row:
                    if (
                        len("".join([last_row_button_text.text
                                     for last_row_button_text in last_row])) <= BUTTON_TEXT_LENGTH_BORDER
                        and len(row) < row_size
                    ):
                        row.append(InlineKeyboardButton(text=button_text,
                                                        callback_data=button_name))
                    else:
                        add_new_row(button_text, button_name)

                    break

        return keyboard_markup


# Exceptions

class RowSizeError(Exception):
    def __init__(self, row_size: int):
        """ Raised when passing an invalid row_size value """
        self.row_size = row_size

    def __str__(self):
        return f"Invalid row_size value: {self.row_size}"