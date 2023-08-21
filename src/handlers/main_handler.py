from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.aiocore import Database
from src.aiocore import ContentManager
from src.aiocore import Keyboard

router = Router()

db = Database()
cm = ContentManager()
kb = Keyboard()


@router.message(Command(commands=["start"]))
async def start_bot(message: types.Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id

    if not db.check_user_exists_in_database(user_id):
        await message.answer("Добро пожаловать!", parse_mode="html")
    else:
        await message.answer(text=cm.get_message_text("start_message", user_id),
                             reply_markup=kb.get_reply_keyboard("main_keyboard", user_id))

    db.add_user_to_database(user_id, message.from_user.username, "ru")
