import re
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar

from Exceptions.ecxeptions import BotExceptions
from Models.models import Product, Order, User, Buyer
from commands import INFO_LIST, WARNING_LIST, ERROR_LIST, SUCCESS_LIST
from loader import dp, bot, bot_logger
from states.make_order import MakeOrder
re_num = r'\d+'


# ========================= ВЫБОР НЕОБХОДИМОГО ПРОДУКТА =============================
@dp.message_handler(state=MakeOrder.choose_product)
async def choose_product(message: types.Message, state: FSMContext):
	"""

	:param message: types.Message
	:param state: FSMContext
	:return:
	"""
	try:
		product_id = re.search(re_num, message.text)

		if product_id:
			product = Product.get(Product.id == product_id[0])
			await state.update_data(product_id=product.id)
			await message.answer(INFO_LIST["selected_product"].format(product.product_name))
			await message.answer(INFO_LIST["set_count"])
			await MakeOrder.set_count.set()
		else:
			await product_search(message, state)
	except ValueError:
		await message.answer(WARNING_LIST["invalid_product"])


# ========================= МЕТОД ПОИСКА =============================
async def product_search(message: types.Message, state: FSMContext):
	"""
	Осуществляет поиск продукта по названию. Если находит подходящий выводит его.
	В случае если продукт не найден сообщает об этом клиенту и перекидывает на следующий щаг
	:param message: types.Message
	:param state: FSMContext
	:return:
	"""
	await message.answer(INFO_LIST["search_in_progress"])
	products = Product.select().where(Product.product_name == message.text)
	if not products.exists():
		await message.answer(INFO_LIST["product_not_exist"])
		await state.update_data(product_id=0)
		await message.answer(INFO_LIST["set_count"])
		await MakeOrder.set_count.set()
	else:
		msg = ''
		for product in products:
			msg += f'{product.id} - {product.product_name}\n'
		await message.answer(msg)


# ========================= УКАЗАНИЕ КОЛИЧЕСТВА ПРОДУКТА =============================
@dp.message_handler(state=MakeOrder.set_count)
async def set_count(message: types.Message, state: FSMContext):
	"""

	:param message: types.Message
	:param state: FSMContext
	:return:
	"""
	try:
		product_count = re.search(re_num, message.text)
		if not product_count:
			await message.answer(ERROR_LIST["fail_count"])
		elif not int(product_count[0]):
			raise BotExceptions.ZeroCount
		else:
			await state.update_data(count=product_count[0])
			calendar, step = DetailedTelegramCalendar().build()
			await message.answer(INFO_LIST["set_limit"], reply_markup=calendar)
			await MakeOrder.set_deadline.set()

	except BotExceptions.ZeroCount:
		await message.answer(ERROR_LIST["zero_count"])


# ========================= УСТАНОВКА КРАЙНЕГО СРОКА =============================
@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=MakeOrder.set_deadline)
async def set_date(call: CallbackQuery, state: FSMContext):
	"""
	Устанавливает крайний срок доставки товара при помощи inline клавиатуры
	:param call: CallbackQuery
	:param state: FSMContext
	:return:
	"""
	result, key, step = DetailedTelegramCalendar().process(call.data)
	if not result and key:
		await bot.edit_message_text(INFO_LIST["set_limit"], call.message.chat.id, call.message.message_id, reply_markup=key)
	elif result:
		await bot.edit_message_text(INFO_LIST["deadline_set"], call.message.chat.id, call.message.message_id)
		deadline = datetime(result.year, result.month, result.day)
		await state.update_data(period=deadline)
		await call.message.answer(INFO_LIST["set_location"])
		await MakeOrder.set_location.set()


# ========================= УКАЗАНИЕ АДРЕСА ДОСТАВКИ =============================
@dp.message_handler(state=MakeOrder.set_location)
async def set_location(message: types.Message, state: FSMContext):
	"""

	:param message: types.Message
	:param state: FSMContext
	:return:
	"""
	location = message.text
	await state.update_data(location=location)
	await message.answer(INFO_LIST["add_comment"])
	await MakeOrder.add_comment.set()


# ========================= ДОБАВЛЕНИЕ КОМЕНТАРИЯ К ЗАЯВКЕ =============================
@dp.message_handler(state=MakeOrder.add_comment)
async def add_comment(message: types.Message, state: FSMContext):
	"""

	:param message: types.Message
	:param state: FSMContext
	:return:
	"""
	comment = message.text
	await state.update_data(comment=comment)
	data = await state.get_data()
	order = Order()

	params = {
		'client_id': message.from_user.id,
		'product_id': data["product_id"],
		'period': data["period"],
		'count': data["count"],
		'comment': data["comment"],
		'location': data["location"],
	}

	try:
		order.add_order(params)
		buyers = Buyer().select()
		for buyer in buyers:
			await bot.send_message(buyer.user.user_id, INFO_LIST["new_order"])

		await message.answer(SUCCESS_LIST["order_added"])
		await state.finish()
	except Exception as ex:
		bot_logger.exception(ex)
		await message.answer(ERROR_LIST["order_adding_fail"])
		await state.finish()
