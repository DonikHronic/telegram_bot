from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
	first_name = State()
	second_name = State()
	patronymic = State()
	email = State()
