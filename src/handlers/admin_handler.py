from aiogram import Router
from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext

from src.aiocore import CoreServices
from src.aiocore.fsm.states import AdminStates, MenuStates

from src.handlers.common.base_answers import BaseAnswers
from src.handlers.common.save_state import save_state

router = Router()


@router.message(AdminStates.first_page, F.text)
async def first_admin_page_handler(message: types.Message, state: FSMContext, core: CoreServices):
    user_id = message.from_user.id
    keyboard_buttons = core.content.get_keyboard_buttons("admin_keyboard", page=1, user_id=user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(core.content, core.keyboard, message, "admin_keyboard")

    button_name = core.keyboard.get_button_name(keyboard_buttons, message.text)

    if button_name == "manage_users_button":
        pass
    elif button_name == "bot_settings_button":
        pass
    elif button_name == "next_page_button":
        await state.set_state(AdminStates.second_page)
        await message.answer(text=core.content.get_message_text("admin_menu", user_id),
                             reply_markup=core.keyboard.get_reply_keyboard("admin_keyboard", user_id, page=2),
                             parse_mode="html")
    elif button_name == "main_menu_button":
        await state.set_state(MenuStates.main_page)
        await message.answer(text=core.content.get_message_text("main", user_id),
                             reply_markup=core.keyboard.get_reply_keyboard("main_keyboard", user_id),
                             parse_mode="html")

    await save_state(core.fsm_storage, user_id, state)


@router.message(AdminStates.second_page, F.text)
async def second_admin_page_handler(message: types.Message, state: FSMContext, core: CoreServices):
    user_id = message.from_user.id
    keyboard_buttons = core.content.get_keyboard_buttons("admin_keyboard", page=2, user_id=user_id)

    if message.text not in keyboard_buttons.values():
        return await BaseAnswers.no_option_answer(core.content, core.keyboard, message, "admin_keyboard")

    button_name = core.keyboard.get_button_name(keyboard_buttons, message.text)

    if button_name == "mailing_menu_button":
        pass
    elif button_name == "analytics_menu_button":
        pass
    elif button_name == "previous_page_button":
        await state.set_state(AdminStates.first_page)
        await message.answer(text=core.content.get_message_text("admin_menu", user_id),
                             reply_markup=core.keyboard.get_reply_keyboard("admin_keyboard", user_id, page=1),
                             parse_mode="html")
    elif button_name == "main_menu_button":
        await state.set_state(MenuStates.main_page)
        await message.answer(text=core.content.get_message_text("main", user_id),
                             reply_markup=core.keyboard.get_reply_keyboard("main_keyboard", user_id),
                             parse_mode="html")

    await save_state(core.fsm_storage, user_id, state)
