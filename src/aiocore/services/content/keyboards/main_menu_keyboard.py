from src.aiocore.content import DataInjector


class MainMenuKeyboardInjector(DataInjector):
    def __init__(self):
        pass

    @DataInjector.check_consistency
    def inject(self, string: str, variables: list[str]):
        return string.format(notifications_count="(1)")
