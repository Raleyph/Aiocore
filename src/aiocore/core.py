from src.aiocore import Content, Keyboard
from src.aiocore import UserRepository
from src.aiocore import FSMStorage


class CoreServices:
    def __init__(
            self,
            user_repository: UserRepository,
            content: Content,
            keyboard: Keyboard,
            fsm_storage: FSMStorage
    ):
        self.user_repository = user_repository
        self.content = content
        self.keyboard = keyboard
        self.fsm_storage = fsm_storage