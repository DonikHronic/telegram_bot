from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from commands import MENU_COMMANDS
from loader import dp


@dp.message_handler(text=MENU_COMMANDS["show_orders"])
async def show_orders(message: types.Message):
	await message.answer('List', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["orders_history"])
async def orders_history(message: types.Message):
	await message.answer('List', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["change_status"])
async def change_status(message: types.Message):
	await message.answer('List', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["refused_orders"])
async def refused_orders(message: types.Message):
	await message.answer('List', reply_markup=ReplyKeyboardRemove())
