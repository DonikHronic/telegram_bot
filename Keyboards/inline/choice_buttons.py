from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Keyboards.inline.callback_datas import user_choice

choice = InlineKeyboardMarkup(row_width=2)

add_client = InlineKeyboardButton(text='Я клиент', callback_data='registration:client')
add_buyer = InlineKeyboardButton(text='Я закупщик', callback_data='registration:buyer')

choice.insert(add_client)
choice.insert(add_buyer)
