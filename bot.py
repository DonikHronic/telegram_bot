from aiogram.utils import executor
from loader import dp, bot, admin_id, configure_logger, bot_logger
from Controllers import SetCommands
import Handlers


async def on_startup(dispatcher):
	await SetCommands.DefaultCommands().set_default_commands(dispatcher)
	await bot.send_message(admin_id, "<i>Бот Запущен</i>")
	bot_logger.info('Bot started')


if __name__ == '__main__':
	configure_logger()
	executor.start_polling(dp, on_startup=on_startup)
