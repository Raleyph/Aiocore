from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    set_language = State()


class MenuStates(StatesGroup):
    main_page = State()


class AdminStates(StatesGroup):
    first_page = State()
    second_page = State()
