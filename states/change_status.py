from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeStatus(StatesGroup):
	set_order_id = State()
	confirm_status = State()
	check_confirm = State()
