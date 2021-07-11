from aiogram import types
from aiogram.dispatcher.filters import Command

from Keyboards.default.menu import menu_client
from commands import COMMANDS_LIST, MENU_COMMANDS
from loader import dp


@dp.message_handler(Command('menu'))
async def show_menu(message: types.Message):
	await message.answer(COMMANDS_LIST["choose_action"], reply_markup=menu_client)


@dp.message_handler(text=MENU_COMMANDS["add_order"])
async def add_order(message: types.Message):
	await message.answer('Hello !!!', reply_markup=types.ReplyKeyboardRemove())
