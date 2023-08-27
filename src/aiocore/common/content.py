from src.content.messages import messages
from src.content.keyboards import keyboards

from src.aiocore.services.database import UserRepository
from src.aiocore import Config

from typing import Optional

MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40


class Content:
    def __init__(self, user_repository: UserRepository, config: Config):
        """ Initialize content manager """
        self.__user_repository = user_repository
        self.__config = config

    def get_message_text(
            self,
            message: str,
            user_id: Optional[int] = None,
            **data
    ) -> str:
        """
        Return message text in user's chosen language

        :param message:
        :param user_id:
        :return:
        """
        if user_id:
            language = self.__user_repository.get_user_data(user_id)[3]
        else:
            language = self.__config.get_parameter("Default", "native_language")

        for message_block in messages:
            if message in message_block:
                current_message: dict[str, str] = message_block[message]

                if language not in current_message:
                    raise MessageLocalizationError(message, language)

                if "variables" in current_message:
                    if not data:
                        raise MessageVariablesError()

                    message_variables = current_message["variables"]

                    for variable in message_variables:
                        if variable not in list(data.keys()):
                            raise MessageVariablesError()

                    final_message = current_message[language].format(**data)
                else:
                    final_message = current_message[language]

                emoji = current_message["emoji"] if "emoji" in current_message else ""

                return f"{final_message} {emoji}"

        raise MessagePresenceError(message)

    def get_keyboard_buttons(
            self,
            keyboard_name: str,
            page: Optional[int] = None,
            user_id: Optional[int] = None
    ) -> dict:
        """
        Return keyboard buttons in user's chosen language

        :param keyboard_name:
        :param page:
        :param user_id:
        :return:
        """
        for keyboard in keyboards:
            if keyboard_name in keyboard:
                keyboard_content = {}

                current_keyboard = keyboard[keyboard_name]

                keyboard_settings: dict = current_keyboard[0]
                keyboard_buttons: dict = current_keyboard[1][0]

                if keyboard_settings["localized"]:
                    if not user_id:
                        localize = self.__config.get_parameter("Default", "native_language")
                    else:
                        localize = self.__user_repository.get_user_data(user_id)[3]
                else:
                    localize = "text"

                if keyboard_settings["paginated"]:
                    if not page:
                        raise

                    keyboard_buttons = keyboard_buttons[page]

                if "optional_buttons" in keyboard_settings:
                    for optional_button in keyboard_settings["optional_buttons"]:
                        if optional_button not in keyboard_buttons:
                            raise

                for button_name, button_content in keyboard_buttons.items():
                    button_text = button_content[localize]
                    button_emoji = button_content["emoji"]

                    if len(button_text) > MAX_KEYBOARD_BUTTON_TEXT_LENGTH:
                        raise KeyboardButtonTextLengthError(button_text)

                    keyboard_content[button_name] = f"{button_text} {button_emoji}"

                return keyboard_content
        else:
            raise KeyboardPresenceError(keyboard_name)


# Exceptions

class MessagePresenceError(Exception):
    def __init__(self, message: str):
        """
        Raised when the requested message construct is not present in the JSON content file

        :param message:
        :return:
        """
        self.message = message

    def __str__(self):
        return f"The requested message construct {self.message} is not present in the JSON content file."


class MessageLocalizationError(Exception):
    def __init__(self, message: str, language: str):
        """
        Raised when the requested message construct does not have the requested
        localization in the JSON content file

        :param message:
        :param language:
        :return:
        """
        self.message = message
        self.language = language

    def __str__(self):
        return f"The requested message construct \"{self.message}\" does not have the " \
               f"requested localization \"{self.language}\" in the JSON content file."


class MessageVariablesError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Penis"


class KeyboardPresenceError(Exception):
    def __init__(self, keyboard_name: str):
        """
        Raised when the requested keyboard construct is not present in the JSON content file

        :param keyboard_name:
        :return:
        """
        self.keyboard_name = keyboard_name

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" is not present in the JSON content file."


class KeyboardLocalizationError(Exception):
    def __init__(self, keyboard_name: str, language: str):
        """
        Raised when the requested keyboard construct does not
        have the requested localization in the JSON content file

        :param keyboard_name:
        :param language:
        :return:
        """
        self.keyboard_name = keyboard_name
        self.language = language

    def __str__(self):
        return f"The requested keyboard construct \"{self.keyboard_name}\" does not have the " \
               f"requested localization \"{self.language}\" in the JSON content file."


class KeyboardButtonTextLengthError(Exception):
    def __init__(self, button_text):
        """
        Raised when the length of the button text exceeds the specified length constant

        :param button_text:
        :return:
        """
        self.button_text = button_text

    def __str__(self):
        return f"The button text \"{self.button_text}\" is too long."
