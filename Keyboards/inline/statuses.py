from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Models.models import Status

statuses = InlineKeyboardMarkup()

accepted = InlineKeyboardButton(text=Status.STATUS_LIST[1][1], callback_data=Status.STATUS_LIST[1][0])
in_process = InlineKeyboardButton(text=Status.STATUS_LIST[2][1], callback_data=Status.STATUS_LIST[2][0])
preparing_for_shipment = InlineKeyboardButton(text=Status.STATUS_LIST[3][1], callback_data=Status.STATUS_LIST[3][0])
sent = InlineKeyboardButton(text=Status.STATUS_LIST[4][1], callback_data=Status.STATUS_LIST[4][0])
statuses.add(accepted)
statuses.add(in_process)
statuses.add(preparing_for_shipment)
statuses.add(sent)
