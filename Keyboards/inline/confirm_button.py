from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from commands import INFO_LIST

confirm = InlineKeyboardMarkup(row_width=1)
confirm_order = InlineKeyboardButton(INFO_LIST["confirm"], callback_data='confirm')
confirm.add(confirm_order)

check_confirm = InlineKeyboardMarkup()
check_yes = InlineKeyboardButton('Да', callback_data='yes')
check_no = InlineKeyboardButton('Нет', callback_data='no')
check_confirm.add(check_yes, check_no)
