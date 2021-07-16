from aiogram.dispatcher.filters.state import StatesGroup, State


class Refusing(StatesGroup):
	set_order_id = State()
	check_refusing = State()
	confirm_refusing = State()
