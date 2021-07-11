from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Keyboards.inline.callback_datas import user_choice
from commands import COMMANDS_LIST

choice = InlineKeyboardMarkup(row_width=2)

add_client = InlineKeyboardButton(text=COMMANDS_LIST['client'], callback_data='registration:client')
add_buyer = InlineKeyboardButton(text=COMMANDS_LIST['buyer'], callback_data='registration:buyer')

choice.insert(add_client)
choice.insert(add_buyer)
