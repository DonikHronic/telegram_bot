from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
	secret_key = State()
	first_name = State()
	second_name = State()
	patronymic = State()
	number = State()
	email = State()
