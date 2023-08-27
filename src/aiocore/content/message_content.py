from src.aiocore.content import DataInjector
from src.aiocore.services.database import UserRepository
from src.aiocore import Config

from src.aiocore.content.injector import InjectorPresenceError

from typing import Optional

MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40


class Content:
    def __init__(
            self,
            user_repository: UserRepository,
            config: Config,
            user_id: int
    ):
        """ Initialize content manager """
        self.__user_repository = user_repository
        self.__config = config
        self.__user_id = user_id

    def get_message_text(
            self,
            message: dict[str, str],
            injector: Optional[DataInjector] = None
    ) -> str:
        """
        Return message text in user's chosen language

        :param message:
        :param injector:
        :return:
        """
        if not self.__user_repository.check_user_exists(self.__user_id):
            language = self.__config.get_parameter("Default", "native_language")
        else:
            language = self.__user_repository.get_user_data(self.__user_id)[3]

        if language not in message:
            raise MessageLocalizationError(message, language)

        if "variables" in message:
            if not injector:
                raise InjectorPresenceError(message)

            final_message = injector.inject(message[language], message["variables"])
        else:
            final_message = message[language]

        emoji = message["emoji"] if "emoji" in message else ""

        return f"{final_message} {emoji}"

    def get_image(self, image):
        pass

    def get_video(self, video):
        pass

    def get_media_group(self):
        pass


# Exceptions

class MessageLocalizationError(Exception):
    def __init__(self, message: str, language: str):
        """
        Raised when the requested message construct does not have the requested
        localization in the message content file

        :param message:
        :param language:
        :return:
        """
        self.message = message
        self.language = language

    def __str__(self):
        return f"The requested message construct \"{self.message}\" does not have the " \
               f"requested localization \"{self.language}\" in the message content file."
