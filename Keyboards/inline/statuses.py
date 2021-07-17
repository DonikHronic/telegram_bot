from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Models.models import Status

statuses = InlineKeyboardMarkup()

in_process = InlineKeyboardButton(text=Status.STATUS_LIST[1][1], callback_data=Status.STATUS_LIST[1][0])
sent = InlineKeyboardButton(text=Status.STATUS_LIST[2][1], callback_data=Status.STATUS_LIST[2][0])
statuses.add(in_process)
statuses.add(sent)
