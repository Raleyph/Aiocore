from src.aiocore.content import InjectorBase


class MainMenuKeyboardInjector(InjectorBase):
    def __init__(self):
        pass

    def inject(self, string: str, variables: list[str]):
        return string.format(notifications_count="(1)")
