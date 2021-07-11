from aiogram import types
from aiogram.dispatcher.filters import Command
from Keyboards.inline.choice_buttons import choice
from commands import COMMANDS_LIST
from loader import dp
from Models.models import User


@dp.message_handler(Command('start'))
async def start_command(message: types.Message):
	user = User()
	check_user = user.is_exist(message.from_user.id)

	if not check_user:
		await message.answer(f'{COMMANDS_LIST["start"]}\n{COMMANDS_LIST["registration"]}', reply_markup=choice)
	else:
		await message.answer(f'{COMMANDS_LIST["start"]}\n{COMMANDS_LIST["exist_registration"]}')
		await message.answer(COMMANDS_LIST["show_actions"])
