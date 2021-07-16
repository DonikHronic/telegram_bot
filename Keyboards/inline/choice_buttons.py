from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from commands import INFO_LIST

choice = InlineKeyboardMarkup(row_width=2)

add_client = InlineKeyboardButton(text=INFO_LIST['client'], callback_data='registration:client')
add_buyer = InlineKeyboardButton(text=INFO_LIST['buyer'], callback_data='registration:buyer')

choice.insert(add_client)
choice.insert(add_buyer)
