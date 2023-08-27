from src.aiocore.content import DataInjector

from src.aiocore import __version__ as aiocore_version
from aiogram import __version__ as aiogram_version


class MainMenuMessageInjector(DataInjector):
    def __init__(self):
        pass

    @DataInjector.check_consistency
    def inject(self, string: str, variables: list[str]):
        return string.format(
            aiocore_version=aiocore_version,
            aiogram_version=aiogram_version
        )
