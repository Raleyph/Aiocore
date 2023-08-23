from aiogram.fsm.context import FSMContext
from src.aiocore import FSMReset


async def save_state(state_storage: FSMReset, user_id: int, state: FSMContext):
    state_storage.save_user_state(
        user_id,
        await state.get_state(),
        await state.get_data()
    )
