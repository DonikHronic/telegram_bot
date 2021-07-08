from aiogram import types, Dispatcher


class DefaultCommands:
	commands_list = [
		('start', 'Запустить бота'),
		('help', 'Вывести справку'),
		('cal', 'календарь'),
		('menu', 'Вывести список действий'),
	]

	async def set_default_commands(self, dispatcher: Dispatcher):
		commands = [types.BotCommand(command, description) for command, description in self.commands_list]
		await dispatcher.bot.set_my_commands(commands)
