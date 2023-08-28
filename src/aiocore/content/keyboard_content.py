from typing import Optional, Union, Any

from src.aiocore import Config
from src.aiocore.content import InjectorBase
from src.aiocore.services.database import UserRepository
from src.aiocore.content.injector import InjectorPresenceError

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, InlineKeyboardButton

MAX_REPLY_ROW_SIZE = 4
MAX_INLINE_ROW_SIZE = 2
MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40
BUTTON_TEXT_LENGTH_BORDER = 15


class Keyboard:
    def __init__(
            self,
            user_repository: UserRepository,
            config: Config,
            user_id: int
    ):
        """ Initialize keyboard object """
        self.__user_repository = user_repository
        self.__config = config
        self.__user_id = user_id

    def __get_keyboard_buttons(
            self,
            keyboard: list[dict[str, Any], list[dict[str, str]]],
            page: Optional[int] = None,
            injector: Optional[InjectorBase] = None
    ):
        """
        Return keyboard buttons in user's chosen language

        :param keyboard:
        :param page:
        :param injector:
        :return:
        """
        keyboard_properties: dict = keyboard[0]
        keyboard_buttons: dict = keyboard[1][0]
        keyboard_name = keyboard_properties["keyboard_name"]

        # Localization

        if keyboard_properties["localized"]:
            if not self.__user_repository.check_user_exists(self.__user_id):
                localize = self.__config.get_parameter("Default", "native_language")
            else:
                localize = self.__user_repository.get_user_data(self.__user_id)[3]
        else:
            localize = "text"

        # Pagination

        if keyboard_properties["paginated"]:
            if not page:
                raise KeyboardPageError(keyboard_name)

            keyboard_buttons = keyboard_buttons[page]

        keyboard_content = {}

        for button_name, button_content in keyboard_buttons.items():
            if localize not in button_content:
                raise KeyboardLocalizationError(keyboard_name, localize)

            # Injection

            if "variables" in button_content:
                if not injector:
                    raise InjectorPresenceError(f"{keyboard_name}:{button_name}")

                button_text = injector.inject(button_content[localize], button_content["variables"])
            else:
                button_text = button_content[localize]

            if len(button_text) > MAX_KEYBOARD_BUTTON_TEXT_LENGTH:
                raise KeyboardButtonTextLengthError(button_text)

            button_emoji = button_content["emoji"]
            keyboard_content[button_name] = f"{button_text} {button_emoji}"

        return keyboard_content

    @staticmethod
    def __markup(
            keyboard_buttons: dict,
            is_inline: bool,
            row_size: int = 2
    ) -> list[Union[KeyboardButton, InlineKeyboardButton]]:
        """
        Return sorted reply or inline keyboard markup

        :param is_inline:
        :param row_size:
        :return:
        """
        max_row_size = MAX_REPLY_ROW_SIZE if not is_inline else MAX_INLINE_ROW_SIZE

        if row_size > max_row_size or row_size < 0:
            raise RowSizeError(row_size)

        keyboard_markup = []

        def get_new_button(new_button_name: str, new_button_text: str):
            if not is_inline:
                button = KeyboardButton(text=new_button_text)
            else:
                button = InlineKeyboardButton(text=new_button_text, callback_data=new_button_name)

            return button

        def add_new_row(button: Union[KeyboardButton, InlineKeyboardButton]):
            keyboard_markup.append([button])

        for button_name, button_text in keyboard_buttons.items():
            new_button = get_new_button(button_name, button_text)

            if (
                len(button_text) > BUTTON_TEXT_LENGTH_BORDER
                or not keyboard_markup
            ):
                add_new_row(new_button)
                continue

            for row in keyboard_markup:
                last_row = keyboard_markup[len(keyboard_markup) - 1]

                if row is last_row:
                    if (
                        len("".join([last_row_button_text.text
                                     for last_row_button_text in last_row])) <= BUTTON_TEXT_LENGTH_BORDER
                        and len(row) < row_size
                    ):
                        row.append(new_button)
                    else:
                        add_new_row(new_button)

                    break

        return keyboard_markup

    def get_keyboard(
            self,
            keyboard: list[dict[str, Any], list[dict[str, str]]],
            is_inline: bool,
            row_size: int = 2,
            page: Optional[int] = None,
            injector: Optional[InjectorBase] = None
    ) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
        """
        Return reply or inline keyboard markup

        :param keyboard:
        :param is_inline:
        :param row_size:
        :param page:
        :param injector:
        :return:
        """
        keyboard_buttons = self.__get_keyboard_buttons(keyboard, page, injector)

        if not is_inline:
            keyboard = ReplyKeyboardBuilder()
            keyboard_markup = self.__markup(keyboard_buttons, is_inline=False, row_size=row_size)
            params = {"resize_keyboard": True}
        else:
            keyboard = InlineKeyboardBuilder()
            keyboard_markup = self.__markup(keyboard_buttons, is_inline=True, row_size=row_size)
            params = {}

        for row in keyboard_markup:
            keyboard.row(*row)

        return keyboard.as_markup(**params)

    def button_callback(
            self,
            button_text: str,
            keyboard: dict,
            page: Optional[int] = None
    ):
        """

        :param button_text:
        :param keyboard:
        :param page:
        :return:
        """
        keyboard_buttons = self.__get_keyboard_buttons(keyboard, page=page)

        if button_text not in keyboard_buttons.values():
            return None

        return dict(zip(keyboard_buttons.values(), keyboard_buttons.keys())).get(button_text)


# Exceptions

class KeyboardPresenceError(Exception):
    def __init__(self, keyboard_name: str):
        """
        Raised when the requested keyboard construct is not present in the keyboard injectors file

        :param keyboard_name:
        :return:
        """
        self.keyboard_name = keyboard_name

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" is not present in the keyboard injectors file."


class KeyboardLocalizationError(Exception):
    def __init__(self, keyboard_name: str, language: str):
        """
        Raised when the requested keyboard construct does not
        have the requested localization in the keyboard injectors file

        :param keyboard_name:
        :param language:
        :return:
        """
        self.keyboard_name = keyboard_name
        self.language = language

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" does not have the " \
               f"requested localization \"{self.language}\" in the keyboard injectors file."


class KeyboardButtonTextLengthError(Exception):
    def __init__(self, button_text: str):
        """
        Raised when the length of the button text exceeds the specified length constant

        :param button_text:
        :return:
        """
        self.button_text = button_text

    def __str__(self):
        return f"The button text \"{self.button_text}\" is too long."


class RowSizeError(Exception):
    def __init__(self, row_size: int):
        """ Raised when passing an invalid row_size value """
        self.row_size = row_size

    def __str__(self):
        return f"Invalid row_size value: {self.row_size}"


class KeyboardPageError(Exception):
    def __init__(self, keyboard_name: str):
        """
        Raised when trying to get a paginated keyboard doesn't provide a page number

        :param keyboard_name:
        """
        self.keyboard_name = keyboard_name

    def __str__(self):
        return f""
