from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram import __version__ as aiogram_version
from src.aiocore import __version__ as aiocore_version

from src.aiocore import CoreServices
from src.aiocore.fsm.states import RegistrationStates, MenuStates

from src.handlers.common.base_answers import BaseAnswers
from src.handlers.common.save_state import save_state

router = Router()


@router.message(Command(commands=["start"]))
async def start_bot(message: types.Message, state: FSMContext, core: CoreServices):
    await state.clear()

    user_id = message.from_user.id

    if not core.user_repository.check_user_exists(user_id):
        core.user_repository.add_user(user_id, message.from_user.username, message.chat.id)

        await state.set_state(RegistrationStates.set_language)
        await message.answer(text=core.content.get_message_text("start"),
                             reply_markup=core.keyboard.get_reply_keyboard("language_keyboard", user_id),
                             parse_mode="html")
    else:
        await state.set_state(MenuStates.main_page)
        await message.answer(text=core.content.get_message_text("main", user_id,
                                                                aiogram_version=aiogram_version,
                                                                aiocore_version=aiocore_version),
                             reply_markup=core.keyboard.get_reply_keyboard("main_keyboard", user_id),
                             parse_mode="html")

    await save_state(core.fsm_storage, user_id, state)


@router.message(RegistrationStates.set_language, F.text)
async def set_user_language(message: types.Message, state: FSMContext, core: CoreServices):
    user_id = message.from_user.id
    keyboard_buttons = core.content.get_keyboard_buttons("language_keyboard", user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(core.content, core.keyboard, message, "main_keyboard")

    language = core.keyboard.get_button_name(keyboard_buttons, message.text)
    core.user_repository.change_user_language(user_id, language)

    await state.set_state(MenuStates.main_page)
    await message.answer(text=core.content.get_message_text("main", user_id),
                         reply_markup=core.keyboard.get_reply_keyboard("main_keyboard", user_id),
                         parse_mode="html")

    await save_state(core.fsm_storage, user_id, state)
