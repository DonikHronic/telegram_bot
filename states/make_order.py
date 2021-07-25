from aiogram.dispatcher.filters.state import StatesGroup, State


class MakeOrder(StatesGroup):
	choose_product = State()
	search_product = State()
	set_count = State()
	set_deadline = State()
	set_location = State()
	add_comment = State()
