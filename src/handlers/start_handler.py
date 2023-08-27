from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.aiocore import CoreServices
from src.aiocore.fsm.states import *

from src.content.messages import *
from src.content.keyboards import *

from src.handlers.common import BaseAnswers

router = Router()


@router.message(Command(commands=["start"]))
async def start_bot(message: types.Message, state: FSMContext, core: CoreServices):
    await state.clear()

    user_id = message.from_user.id

    if not core.user_repository.check_user_exists(user_id):
        await state.set_state(RegistrationStates.set_language)
        await message.answer(text=core.content.get_message_text(start_message),
                             reply_markup=core.keyboard.get_keyboard(
                                 keyboard=set_language_keyboard,
                                 is_inline=False
                             ),
                             parse_mode="html")

        core.user_repository.add_user(user_id, message.from_user.username, message.chat.id)
    else:
        await state.set_state(MenuStates.main_page)
        await BaseAnswers.main_menu_answer(core.content, core.keyboard, message)


@router.message(RegistrationStates.set_language, F.text)
async def set_user_language(message: types.Message, state: FSMContext, core: CoreServices):
    user_id = message.from_user.id
    keyboard_buttons = core.keyboard.get_keyboard_buttons(set_language_keyboard, user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(core.content, core.keyboard, message, set_language_keyboard)

    language = core.keyboard.get_button_name(keyboard_buttons, message.text)
    core.user_repository.change_user_language(user_id, language)

    await state.set_state(MenuStates.main_page)
    await BaseAnswers.main_menu_answer(core.content, core.keyboard, message)
