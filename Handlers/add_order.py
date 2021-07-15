from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar

from Models.models import Product, Order
from commands import INFO_LIST, WARNING_LIST, ERROR_LIST, SUCCESS_LIST
from loader import dp, bot
from states.make_order import MakeOrder


@dp.message_handler(state=MakeOrder.choose_product)
async def choose_product(message: types.Message, state: FSMContext):
	data = await state.get_data()
	try:
		number = int(message.text)
		if number <= data['products_count']:
			product = Product.get(Product.id == number)
			await state.update_data(product_id=product.id)
			await message.answer(INFO_LIST["selected_product"].format(product.product_name))
			await message.answer(INFO_LIST["set_count"])
			await MakeOrder.set_count.set()
		else:
			await message.answer(WARNING_LIST["invalid_product"])
	except ValueError:
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


@dp.message_handler(state=MakeOrder.set_count)
async def set_count(message: types.Message, state: FSMContext):
	try:
		product_count = int(message.text)
		await state.update_data(count=product_count)
		calendar, step = DetailedTelegramCalendar().build()
		await message.answer(INFO_LIST["set_limit"], reply_markup=calendar)
		await MakeOrder.set_deadline.set()
	except ValueError:
		await message.answer(ERROR_LIST["fail_count"])


@dp.callback_query_handler(DetailedTelegramCalendar.func(), state=MakeOrder.set_deadline)
async def set_date(call: CallbackQuery, state: FSMContext):
	result, key, step = DetailedTelegramCalendar().process(call.data)
	if not result and key:
		await bot.edit_message_text(INFO_LIST["set_limit"], call.message.chat.id, call.message.message_id, reply_markup=key)
	elif result:
		await bot.edit_message_text(INFO_LIST["deadline_set"], call.message.chat.id, call.message.message_id)
		deadline = datetime(result.year, result.month, result.day)
		await state.update_data(period=deadline)
		await call.message.answer(INFO_LIST["add_comment"])
		await MakeOrder.add_comment.set()


@dp.message_handler(state=MakeOrder.add_comment)
async def add_comment(message: types.Message, state: FSMContext):
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
	}

	order.add_order(params)
	await message.answer(SUCCESS_LIST["order_added"])
