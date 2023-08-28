from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    set_language = State()


class MenuStates(StatesGroup):
    main_page = State()
