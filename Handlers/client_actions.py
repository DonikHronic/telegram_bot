from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageTextIsEmpty

from Keyboards.inline.confirm_button import confirm, check_confirm
from Models.models import Product, User, Order, Client, Status
from commands import MENU_COMMANDS, INFO_LIST, ERROR_LIST, WARNING_LIST
from loader import dp, bot_logger
from states.confirmation import Confirmation
from states.make_order import MakeOrder
from states.refusing_order import Refusing


# ========================= ДОБАВЛЕНИЕ ЗАЯВКИ =============================
@dp.message_handler(text=MENU_COMMANDS["add_order"])
async def add_order(message: types.Message):
	items = Product.select()
	msg = ''
	for item in items:
		if not item.id:
			msg += f'{item.id} - {item.product_name}\n'

	await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
	await message.answer(INFO_LIST["choose_product"])
	await MakeOrder.choose_product.set()


# ========================= МОИ ЗАЯВКИ =============================
@dp.message_handler(text=MENU_COMMANDS["my_orders"])
async def my_orders(message: types.Message):
	try:
		client = Client.select().join(User).where(User.user_id == message.from_user.id).get()
		orders = Order.select().where(Order.client == client.id, Order.refuse == 0)
		msg = ''
		orders_for_confirm = []
		for order in orders:
			if order.status.status_name not in Status.STATUS_LIST[2][1]:
				msg += f'''
					{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
					\n{"":=<25}\n\n
				'''
			else:
				mess = f'''
					{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
				'''
				orders_for_confirm.append(mess)

		await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())

		for order in orders_for_confirm:
			await message.answer(order, reply_markup=confirm)
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders"])
	except Exception as ex:
		bot_logger.exception(ex)
		await message.answer(ERROR_LIST["fail_show_orders"])


# ========================= ОТМЕНИТЬ ЗАЯВКУ =============================
@dp.message_handler(text=MENU_COMMANDS["refuse_order"])
async def refuse_order(message: types.Message):
	try:
		client = Client.select().join(User).where(User.user_id == message.from_user.id).get()
		orders = Order.select().where(Order.client == client.id, Order.refuse == 0)
		msg = ''
		for order in orders:
			if order.status.status_name != Status.STATUS_LIST[2][1] and order.status.status_name != Status.STATUS_LIST[3][1]:
				msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
					\n{"":=<25}\n\n
				'''
		await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
		await message.answer(INFO_LIST["set_order_id"])
		await Refusing.set_order_id.set()
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders_refuse"], reply_markup=types.ReplyKeyboardRemove())
	except Exception as ex:
		bot_logger.exception(ex)
		await message.answer(ERROR_LIST["refuse_order"])


@dp.message_handler(state=Refusing.set_order_id)
async def refusing_id(message: types.Message, state: FSMContext):
	try:
		order_id = int(message.text)
		await state.update_data(order_id=order_id)
		await message.answer(WARNING_LIST["check_refusing"], reply_markup=check_confirm)
		await Refusing.confirm_refusing.set()
	except ValueError:
		await message.answer(WARNING_LIST["invalid_order_id"])


@dp.callback_query_handler(text='yes', state=Refusing.confirm_refusing)
async def yes_confirm(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	order_id = data["order_id"]
	order = Order.update({Order.refuse: True}).where(Order.id == order_id)
	order.execute()
	order_info = Order.get_by_id(order_id)
	await call.message.answer(INFO_LIST["refused"].format(order_info.product.product_name, order_info.count))
	await state.finish()


@dp.callback_query_handler(text='no', state=Refusing.confirm_refusing)
async def yes_confirm(call: CallbackQuery, state: FSMContext):
	await call.message.answer(INFO_LIST["refuse_decline"])
	await state.finish()


# ========================= СВЯЗАТЬСЯ С ЗАКУПШИКОМ =============================
@dp.message_handler(text=MENU_COMMANDS["connect_buyer"])
async def connect_buyer(message: types.Message):
	await message.answer('@Shamshodkhon', reply_markup=types.ReplyKeyboardRemove())


# ========================= ПОДТВЕРДИТЬ ПОЛУЧЕНИЕ ЗАЯВКИ =============================
@dp.callback_query_handler(text='confirm')
async def confirm_order(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(order=call.message.text)
	await call.message.answer(INFO_LIST['check_confirm'], reply_markup=check_confirm)
	await Confirmation.confirm.set()


@dp.callback_query_handler(text='yes', state=Confirmation.confirm)
async def yes_confirm(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	order_id = int(data["order"][0])
	order = Order.update({Order.status: 4}).where(Order.id == order_id)
	order.execute()
	await call.message.answer(INFO_LIST['confirmed'])
	await state.finish()


@dp.callback_query_handler(text='no', state=Confirmation.confirm)
async def yes_confirm(call: CallbackQuery, state: FSMContext):
	await call.message.answer(WARNING_LIST["not_confirmed"])
	await state.finish()
