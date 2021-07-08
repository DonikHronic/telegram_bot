from aiogram import types
from aiogram.dispatcher.filters import Command
from Keyboards.inline.choice_buttons import choice
from loader import dp


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
	await message.answer(f'Приветствую в боте', reply_markup=choice)
