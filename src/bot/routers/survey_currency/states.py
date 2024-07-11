from aiogram.fsm.state import StatesGroup, State


class Survey(StatesGroup):
    currency = State()
    min = State()
    max = State()
