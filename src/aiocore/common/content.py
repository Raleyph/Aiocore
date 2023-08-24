from typing import Optional

import json
import sys
import os

MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40


class Content:
    __TEXT_CONTENT_FILE_PATH = "src/bot_content.json"

    def __init__(self, user_repository, config):
        """ Initialize content manager """
        content_file_path = os.path.join(sys.path[1], self.__TEXT_CONTENT_FILE_PATH)

        if not os.path.exists(content_file_path):
            raise ContentFileError()

        self.json_data = json.load(open(content_file_path, encoding="utf-8"))
        self.user_repository = user_repository
        self.config = config

    def get_message_text(
            self,
            message: str,
            user_id: Optional[int] = None
    ) -> str:
        """
        Return message text in user's chosen language

        :param message:
        :param user_id:
        :return:
        """
        messages = self.json_data["messages"]

        if user_id:
            language = self.user_repository.get_user_data(user_id)[3]
        else:
            language = self.config.get_parameter("Default", "native_language")

        for message_block in messages:
            if message in message_block:
                if language not in message_block[message]:
                    raise MessageLocalizationError(message, language)

                return message_block[message][language]

        raise MessagePresenceError(message)

    def get_keyboard_buttons(
            self,
            keyboard_name: str,
            user_id: Optional[int] = None
    ) -> dict:
        """
        Return keyboard buttons in user's chosen language

        :param keyboard_name:
        :param user_id:
        :return:
        """
        for keyboard in [*self.json_data["keyboards"]]:
            if keyboard_name in keyboard:
                keyboard_content = {}

                current_keyboard = keyboard[keyboard_name]

                keyboard_settings: dict = current_keyboard[0]
                keyboard_buttons: dict = current_keyboard[1]

                if keyboard_settings["localized"]:
                    if not user_id:
                        localize = self.config.get_parameter("Default", "native_language")
                    else:
                        localize = self.user_repository.get_user_data(user_id)[3]
                else:
                    localize = "text"

                for button_name, button_content in keyboard_buttons.items():
                    button_text = button_content[localize]
                    button_emoji = button_content["emoji"]

                    if len(button_text) > MAX_KEYBOARD_BUTTON_TEXT_LENGTH:
                        raise KeyboardButtonTextLengthError(button_text)

                    keyboard_content[button_name] = f"{button_text} {button_emoji}"

                return keyboard_content
        else:
            raise KeyboardPresenceError(keyboard_name)

    def get_image(self):
        pass


# Exceptions

class ContentFileError(Exception):
    def __init__(self):
        """ Raise when the JSON content file path does not exist in the main project directory """
        pass

    def __str__(self):
        return "The JSON content file does not exists in main project directory."


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
