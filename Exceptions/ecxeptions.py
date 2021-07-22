class BotExceptions:
	class ZeroCount(Exception):
		def __init__(self):
			self.message = 'Установка нулевого значения для количества продукта'

		def __str__(self):
			return self.message

