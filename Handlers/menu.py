from aiogram import types
from aiogram.dispatcher.filters import Command

from Keyboards.default.menu import menu
from loader import dp


@dp.message_handler(Command('menu'))
async def show_menu(message: types.Message):
	await message.answer('Выберите действие которое хотите выплонить', reply_markup=menu)


@dp.message_handler(text='Добавить заявку')
async def add_order(message: types.Message):
	await message.answer('Hello !!!', reply_markup=types.ReplyKeyboardRemove())
