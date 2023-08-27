from typing import Optional, Union, Any

from src.aiocore.content import DataInjector
from src.aiocore.services.database import UserRepository
from src.aiocore import Config

from src.aiocore.content.injector import InjectorPresenceError

from src.aiocore.content.keyboard_markup import KeyboardMarkup

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup

MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40


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

    def get_keyboard_buttons(
            self,
            keyboard: list[dict[str, Any], list[dict[str, str]]],
            page: Optional[int] = None,
            injector: Optional[DataInjector] = None
    ):
        """
        Return keyboard buttons in user's chosen language

        :param keyboard:
        :param page:
        :param injector:
        :return:
        """
        keyboard_content = {}

        keyboard_properties: dict = keyboard[0]
        keyboard_buttons: dict = keyboard[1][0]

        keyboard_name = keyboard_properties["keyboard_name"]

        if keyboard_properties["localized"]:
            if not self.__user_repository.check_user_exists(self.__user_id):
                localize = self.__config.get_parameter("Default", "native_language")
            else:
                localize = self.__user_repository.get_user_data(self.__user_id)[3]
        else:
            localize = "text"

        if keyboard_properties["paginated"]:
            if not page:
                raise KeyboardPageError(keyboard_name)

            keyboard_buttons = keyboard_buttons[page]

        for button_name, button_content in keyboard_buttons.items():
            if localize not in button_content:
                raise KeyboardLocalizationError(keyboard_name, localize)

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

    def get_keyboard(
            self,
            keyboard: list[dict[str, Any], list[dict[str, str]]],
            is_inline: bool,
            row_size: int = 2,
            page: Optional[int] = None,
            injector: Optional[DataInjector] = None
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
        markup = KeyboardMarkup(self.get_keyboard_buttons(keyboard, page, injector))

        if not is_inline:
            keyboard = ReplyKeyboardBuilder()
            keyboard_markup = markup.get_reply_keyboard_markup(row_size)
            params = {"resize_keyboard": True}
        else:
            keyboard = InlineKeyboardBuilder()
            keyboard_markup = markup.get_inline_keyboard_markup(row_size)
            params = {}

        for row in keyboard_markup:
            keyboard.row(*row)

        return keyboard.as_markup(**params)

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


# Exceptions

class KeyboardPresenceError(Exception):
    def __init__(self, keyboard_name: str):
        """
        Raised when the requested keyboard construct is not present in the keyboard content file

        :param keyboard_name:
        :return:
        """
        self.keyboard_name = keyboard_name

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" is not present in the keyboard content file."


class KeyboardLocalizationError(Exception):
    def __init__(self, keyboard_name: str, language: str):
        """
        Raised when the requested keyboard construct does not
        have the requested localization in the keyboard content file

        :param keyboard_name:
        :param language:
        :return:
        """
        self.keyboard_name = keyboard_name
        self.language = language

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" does not have the " \
               f"requested localization \"{self.language}\" in the keyboard content file."


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


class KeyboardPageError(Exception):
    def __init__(self, keyboard_name: str):
        """
        Raised when trying to get a paginated keyboard doesn't provide a page number

        :param keyboard_name:
        """
        self.keyboard_name = keyboard_name

    def __str__(self):
        return f""
