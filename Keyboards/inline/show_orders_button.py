from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from commands import INFO_LIST

show_orders_btn = InlineKeyboardMarkup(row_width=3)

show_all_orders = InlineKeyboardButton(text=INFO_LIST["show_all_orders"], callback_data='show:all')
show_complete_orders = InlineKeyboardButton(text=INFO_LIST["show_complete_orders"], callback_data='show:complete')
show_new_orders = InlineKeyboardButton(text=INFO_LIST["show_new_orders"], callback_data='show:new')

show_orders_btn.add(show_all_orders)
show_orders_btn.add(show_complete_orders)
show_orders_btn.add(show_new_orders)
