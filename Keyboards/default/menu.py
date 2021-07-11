from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from commands import MENU_COMMANDS

menu_client = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text=MENU_COMMANDS["add_order"]),
			KeyboardButton(text=MENU_COMMANDS["my_orders"])
		],
		[
			KeyboardButton(text=MENU_COMMANDS["refuse_orders"]),
			KeyboardButton(text=MENU_COMMANDS["connect_buyer"])
		]
	],
	resize_keyboard=True
)

menu_buyer = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text=MENU_COMMANDS['show_orders']),
			KeyboardButton(text=MENU_COMMANDS['orders_history'])
		],
		[
			KeyboardButton(text=MENU_COMMANDS['change_status']),
			KeyboardButton(text=MENU_COMMANDS['refused_orders'])
		]
	],
	resize_keyboard=True
)
