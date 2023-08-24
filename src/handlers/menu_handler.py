from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext

from src.aiocore import CoreServices

from src.aiocore.fsm.states import MenuStates

from src.handlers.common.base_answers import BaseAnswers
from src.handlers.common.save_state import save_state

router = Router()


@router.message(MenuStates.main_page, F.text)
async def main_menu_handler(message: types.Message, state: FSMContext, core: CoreServices):
    user_id = message.from_user.id
    await save_state(core.fsm_storage, user_id, state)

    keyboard_buttons = core.content.get_keyboard_buttons("main_keyboard", user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(core.content, core.keyboard, message, "main_keyboard", user_id)

    button_name = core.keyboard.get_button_name(keyboard_buttons, message.text)

    if button_name == "info_button":
        await message.answer(text=core.content.get_message_text("info_about_bot", user_id),
                             parse_mode="html")
    elif button_name == "":
        pass
    elif button_name == "":
        pass
    elif button_name == "":
        pass
