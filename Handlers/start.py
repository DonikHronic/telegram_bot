from aiogram import types
from aiogram.dispatcher.filters import Command
from Keyboards.inline.choice_buttons import choice
from commands import INFO_LIST
from loader import dp
from Models.models import User


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
	user = User()
	check_user = user.is_exist(message.from_user.id)

	if not check_user:
		await message.answer(f'{INFO_LIST["start"]}\n{INFO_LIST["registration"]}', reply_markup=choice)
	else:
		await message.answer(f'{INFO_LIST["start"]}\n{INFO_LIST["exist_registration"]}')
		await message.answer(INFO_LIST["show_actions"])
