from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('help'))
async def help_handle(message: types.Message):
	help_text = '''
					Список команд:
					\t/start - Запуск бота
					\t/help - Вызов справки
				'''
	await message.answer(help_text)
