from aiogram.fsm.state import StatesGroup, State


class Choice(StatesGroup):
    photo = State()
    string = State()
