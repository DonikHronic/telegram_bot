import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

admin_id = config.ADMIN
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

bot_logger = logging.getLogger('bot_logger')
bot_logger.setLevel(logging.DEBUG)


def configure_logger():
	console_formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
	stream_handler = logging.StreamHandler()
	stream_handler.setFormatter(console_formatter)
	stream_handler.setLevel(logging.DEBUG)
	bot_logger.addHandler(stream_handler)

	file_formatter = logging.Formatter(
		'[%(asctime)s] - %(filename)s [LINE:%(lineno)d] - %(levelname)s - %(message)s',
		'%d-%m-%Y, %H:%M:%S'
	)
	file_handler = logging.FileHandler('bot.log', mode='a', encoding='utf8')
	file_handler.setFormatter(file_formatter)
	file_handler.setLevel(logging.INFO)
	bot_logger.addHandler(file_handler)
