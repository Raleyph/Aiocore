from src.aiocore import Config
from src.aiocore.content import InjectorBase
from src.aiocore.services.database import UserRepository
from src.aiocore.content.injector import InjectorPresenceError, InjectError

from typing import Optional

MAX_KEYBOARD_BUTTON_TEXT_LENGTH = 40


class Content:
    def __init__(
            self,
            user_repository: UserRepository,
            config: Config,
            user_id: int
    ):
        """ Initialize injectors manager """
        self.__user_repository = user_repository
        self.__config = config
        self.__user_id = user_id

    def get_message_text(
            self,
            message: dict[str, str],
            injector: Optional[InjectorBase] = None
    ) -> str:
        """
        Return message text in user's chosen language

        :param message:
        :param injector:
        :return:
        """

        # Localization

        language = self.__config.get_parameter("Default", "native_language")

        if self.__user_repository.check_user_exists(self.__user_id):
            if self.__user_repository.get_user_data(self.__user_id)[3]:
                language = self.__user_repository.get_user_data(self.__user_id)[3]

        if language not in message:
            raise MessageLocalizationError(message, language)

        # Injection

        if "variables" in message:
            if not injector:
                raise InjectorPresenceError(message)

            final_message = injector.inject(message[language], message["variables"])

            if not final_message:
                raise InjectError()
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
