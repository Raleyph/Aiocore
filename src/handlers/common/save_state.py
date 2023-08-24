from aiogram.fsm.context import FSMContext
from src.aiocore import FSMStorage


async def save_state(state_storage: FSMStorage, user_id: int, state: FSMContext):
    state_storage.save_user_state(
        user_id,
        await state.get_state(),
        await state.get_data()
    )
