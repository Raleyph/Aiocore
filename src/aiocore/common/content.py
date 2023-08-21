from src.aiocore import Database

import json
import sys
import os


class ContentManager:
    __TEXT_CONTENT_FILE_PATH = "src/bot_content.json"
    __MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40

    def __init__(self):
        """ Initialize content manager """
        content_file_path = os.path.join(sys.path[1], self.__TEXT_CONTENT_FILE_PATH)

        if not os.path.exists(content_file_path):
            raise ContentFileError()

        self.json_data = json.load(open(content_file_path, encoding="utf-8"))
        self.database = Database()

    def get_message_text(
            self,
            message: str,
            user_id: int
    ) -> str:
        """
        Return message text in user's chosen language

        :param message:
        :param user_id:
        :return:
        """
        messages = self.json_data["messages"]
        language = self.database.get_user_data(user_id)[3]

        for message_block in messages:
            if message in message_block:
                if language not in message_block[message]:
                    raise MessageLocalizationError(message, language)

                return message_block[message][language]

        raise MessagePresenceError(message)

    def get_keyboard_buttons_text(
            self,
            keyboard_name: str,
            is_inline_keyboard: bool,
            user_id: int
    ) -> list:
        """
        Return keyboard buttons in user's chosen language

        :param keyboard_name:
        :param is_inline_keyboard:
        :param user_id:
        :return:
        """
        for keyboard in [
            *self.json_data["reply_keyboards"],
            *self.json_data["inline_keyboards"]
        ]:
            if keyboard_name in keyboard:
                keyboard_content = []
                language = self.database.get_user_data(user_id)[3]

                for button in keyboard[keyboard_name]:
                    for button_content in button.values():

                        button_text = button_content[language]
                        button_emoji = button_content['emoji']

                        if language not in button_content:
                            raise KeyboardLocalizationError(keyboard_name, language)

                        if len(button_text) > self.__MAX_KEYBOARD_BUTTON_TEXT_LENGTH:
                            raise KeyboardButtonTextLengthError(button_text)

                        if not is_inline_keyboard:
                            keyboard_content.append(f"{button_text} {button_emoji}")
                        else:
                            keyboard_content.append({f"{list(button.keys())[0]}":
                                                     f"{button_text} {button_emoji}"})

                return keyboard_content
        else:
            raise KeyboardPresenceError(keyboard_name)


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
