from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.exceptions import MessageTextIsEmpty

from Keyboards.inline.callback_datas import buyer_order_show
from Keyboards.inline.confirm_button import check_confirm
from Keyboards.inline.show_orders_button import show_orders_btn
from Keyboards.inline.statuses import statuses
from Models.models import Order, Status
from commands import MENU_COMMANDS, INFO_LIST, WARNING_LIST, SUCCESS_LIST
from loader import dp
from states.change_status import ChangeStatus


@dp.message_handler(text=MENU_COMMANDS["show_orders_btn"])
async def show_orders(message: types.Message):
	"""
	Выводит клавиатуру для выбора типа вывода заявок
	:param message: types.Message
	:return:
	"""
	await message.answer(INFO_LIST["show_orders_btn"], reply_markup=ReplyKeyboardRemove())
	await message.answer(INFO_LIST["choose_showing"], reply_markup=show_orders_btn)


@dp.callback_query_handler(buyer_order_show.filter(order='all'))
async def show_all_orders(call: CallbackQuery):
	"""
	Выводит все заявки кроме отмененных
	:param call: CallbackQuery
	:return:
	"""
	await call.answer(cache_time=60)
	msg = ''
	orders = Order.select().where(Order.refuse == 0)
	for order in orders:
		msg += f'''{order.id} - {order.product.product_name}
			Количество: {order.count}
			Статус: {order.status.status_name}
			Комментарий: {order.comment}
		'''
		msg += f'\n{"":=<25}\n\n'
	await call.message.answer(msg)


@dp.callback_query_handler(buyer_order_show.filter(order='complete'))
async def show_complete_orders(call: CallbackQuery):
	"""
	Выводит завершенные заявки
	:param call: CallbackQuery
	:return:
	"""
	await call.answer(cache_time=60)
	try:
		msg = ''
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[3][1])
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
				Количество: {order.count}
				Статус: {order.status.status_name}
				Комментарий: {order.comment}
			'''
			msg += f'\n{"":=<25}\n\n'
		await call.message.answer(msg)
	except MessageTextIsEmpty:
		await call.message.answer(WARNING_LIST["not_have_orders"])


@dp.callback_query_handler(buyer_order_show.filter(order='new'))
async def show_complete_orders(call: CallbackQuery):
	"""
	Выводит все заявки со статусом: Принята
	:param call: CallbackQuery
	:return:
	"""
	await call.answer(cache_time=60)
	try:
		msg = ''
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[0][1])
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
				Количество: {order.count}
				Статус: {order.status.status_name}
				Комментарий: {order.comment}
			'''
			msg += f'\n{"":=<25}\n\n'
		await call.message.answer(msg)
	except MessageTextIsEmpty:
		await call.message.answer(WARNING_LIST["not_have_orders"])


@dp.message_handler(text=MENU_COMMANDS["orders_history"])
async def orders_history(message: types.Message):
	"""
	Выводит завершенные заявки
	:param message: types.Message
	:return:
	"""
	try:
		msg = ''
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[3][1])
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
				'''
			msg += f'\n{"":=<25}\n\n'
		await message.answer(msg, reply_markup=ReplyKeyboardRemove())
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders"], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["refused_orders"])
async def refused_orders(message: types.Message):
	"""
	Выводит отмененные заявки
	:param message: types.Message
	:return:
	"""
	msg = ''
	orders = Order.select().where(Order.refuse)
	for order in orders:
		msg += f'''{order.id} - {order.product.product_name}
				Количество: {order.count}
				Статус: {order.status.status_name}
				Комментарий: {order.comment}
			'''
		msg += f'\n{"":=<25}\n\n'
	await message.answer(msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["change_status"])
async def change_status(message: types.Message):
	msg = ''
	orders = Order.select().join(Status).where(Status.status_name != Status.STATUS_LIST[-1][1])
	for order in orders:
		msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
				'''
		msg += f'\n{"":=<25}\n\n'
	await message.answer(msg, reply_markup=ReplyKeyboardRemove())
	await ChangeStatus.set_order_id.set()


@dp.message_handler(state=ChangeStatus.set_order_id)
async def set_status(message: types.Message, state: FSMContext):
	try:
		order_id = int(message.text)
		await state.update_data(order_id=order_id)
		await message.answer(INFO_LIST["change_status"], reply_markup=statuses)
		await ChangeStatus.confirm_status.set()
	except ValueError:
		await message.answer(WARNING_LIST["invalid_order_id"])


@dp.callback_query_handler(state=ChangeStatus.confirm_status)
async def confirm_status(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	for status in Status.STATUS_LIST:
		if call.data in status:
			await state.update_data(status=status[-1])
			await call.message.answer(INFO_LIST["confirm_status"].format(status[-1]), reply_markup=check_confirm)
			await ChangeStatus.check_confirm.set()


@dp.callback_query_handler(state=ChangeStatus.check_confirm)
async def checks_confirm(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	if call.data == 'yes':
		data = await state.get_data()
		order_id = data["order_id"]
		status_id = Status.get(Status.status_name == data["status"])
		order = Order.update({Order.status: status_id}).where(Order.id == order_id)
		order.execute()
		await call.message.answer(SUCCESS_LIST["change_success"])
		await state.finish()
	else:
		await call.message.answer(INFO_LIST["change_canceled"])
		await state.finish()
