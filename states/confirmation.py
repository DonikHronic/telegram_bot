from aiogram.dispatcher.filters.state import StatesGroup, State


class Confirmation(StatesGroup):
	confirm = State()
