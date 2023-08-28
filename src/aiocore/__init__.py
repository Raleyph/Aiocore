from src.aiocore.database.database import Database
from src.aiocore.common.config import Config
from src.aiocore.common.logger import Logger

"""
The UserRepository service is a basic service required for the correct
operation of the FSMStorage, Content and Keyboard modules.
"""

from src.aiocore.services.database import UserRepository

from src.aiocore.content.message_content import Content
from src.aiocore.content.keyboard_content import Keyboard
from src.aiocore.fsm.reset import FSMStorage

from src.aiocore.core import CoreServices

__all__ = [
    "__version__",
    "Database",
    "Config",
    "Logger",
    "Content",
    "Keyboard",
    "FSMStorage",
    "CoreServices"
]

__version__ = "0.2b"
