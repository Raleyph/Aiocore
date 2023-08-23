from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot import users, content, keyboard

from src.aiocore.fsm.states import RegistrationStates, MenuStates

from src.handlers.common.base_answers import BaseAnswers

router = Router()


@router.message(Command(commands=["start"]))
async def start_bot(message: types.Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id

    if not users.check_user_exists(user_id):
        await state.set_state(RegistrationStates.set_language)
        await message.answer(text=content.get_message_text("start"),
                             reply_markup=keyboard.get_reply_keyboard("language_keyboard", user_id),
                             parse_mode="html")
    else:
        await state.set_state(MenuStates.main_page)
        await message.answer(text=content.get_message_text("main", user_id),
                             reply_markup=keyboard.get_reply_keyboard("main_keyboard", user_id),
                             parse_mode="html")


@router.message(RegistrationStates.set_language, F.text)
async def set_user_language(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyboard_buttons = content.get_keyboard_buttons("language_keyboard", user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(message, "language_keyboard")

    language = keyboard.get_button_name(keyboard_buttons, message.text)
    users.add_user(user_id, message.from_user.username, language, message.chat.id)

    await state.set_state(MenuStates.main_page)
    await message.answer(text=content.get_message_text("main", user_id),
                         reply_markup=keyboard.get_reply_keyboard("main_keyboard", user_id),
                         parse_mode="html")
