from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text='Добавить заявку'),
			KeyboardButton(text='В процессе закупа')
		],
		[
			KeyboardButton(text='История закупов')
		]
	],
	resize_keyboard=True
)
