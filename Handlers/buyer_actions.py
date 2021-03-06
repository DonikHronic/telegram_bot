import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.exceptions import MessageTextIsEmpty
from peewee import DoesNotExist

from Exceptions.ecxeptions import BotExceptions
from Keyboards.inline.callback_datas import buyer_order_show
from Keyboards.inline.confirm_button import check_confirm
from Keyboards.inline.show_orders_button import show_orders_btn
from Keyboards.inline.statuses import statuses
from Models.models import Order, Status, Client, User
from commands import MENU_COMMANDS, INFO_LIST, WARNING_LIST, SUCCESS_LIST, ERROR_LIST
from loader import dp, bot_logger, bot
from states.change_status import ChangeStatus


# ========================= ВЫВОД КЛАВИАТУРЫ ДЛЯ ПРОСМОТРА ЗАЯВОК =============================
@dp.message_handler(text=MENU_COMMANDS["show_orders_btn"])
async def show_orders(message: types.Message):
	"""
	Выводит клавиатуру для выбора типа вывода заявок
	:param message: types.Message
	:return:
	"""
	await message.answer(INFO_LIST["show_orders_btn"], reply_markup=ReplyKeyboardRemove())
	await message.answer(INFO_LIST["choose_showing"], reply_markup=show_orders_btn)


# ========================= ВЫВОД ВСЕХ ЗАЯВОК =============================
@dp.callback_query_handler(buyer_order_show.filter(order='all'))
async def show_all_orders(call: CallbackQuery):
	"""
	Выводит все заявки кроме отмененных
	:param call: CallbackQuery
	:return:
	"""
	await call.answer(cache_time=60)
	try:
		msg = ''
		orders = Order.select().where(Order.refuse == 0)
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
					Адрес доставки: {order.location}
					Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
					\n{"":=<25}\n\n
				'''
		await call.message.answer(msg)
	except MessageTextIsEmpty:
		await call.message.answer(WARNING_LIST["not_have_orders"])
	except Exception as ex:
		await call.message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


# ========================= ФИЛЬТРАЦИЯ ЗАВЕРШЁННЫХ ЗАЯВОК =============================
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
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[-1][1])
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
				Количество: {order.count}
				Статус: {order.status.status_name}
				Комментарий: {order.comment}
				Адрес доставки: {order.location}
				Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
				\n{"":=<25}\n\n
			'''
		await call.message.answer(msg)
	except MessageTextIsEmpty:
		await call.message.answer(WARNING_LIST["not_have_orders"])
	except Exception as ex:
		await call.message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


# ========================= ФИЛЬТРАЦИЯ НОВЫХ ЗАЯВОК =============================
@dp.callback_query_handler(buyer_order_show.filter(order='new'))
async def show_complete_orders(call: CallbackQuery):
	"""
	Выводит все заявки со статусом: Еще не принята
	:param call: CallbackQuery
	:return:
	"""
	await call.answer(cache_time=60)
	try:
		msg = ''
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[0][1])
		for order in orders:
			if not order.refuse:
				msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
					Адрес доставки: {order.location}
					Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
					\n{"":=<25}\n\n
				'''
		await call.message.answer(msg)
	except MessageTextIsEmpty:
		await call.message.answer(WARNING_LIST["not_have_orders"])
	except DoesNotExist:
		await call.message.answer(WARNING_LIST["not_have_orders"])
	except Exception as ex:
		await call.message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


# ========================= ВЫВОД ИСТОРИИ ЗАЯВОК =============================
@dp.message_handler(text=MENU_COMMANDS["orders_history"])
async def orders_history(message: types.Message):
	"""
	Выводит завершенные заявки
	:param message: types.Message
	:return:
	"""
	try:
		msg = ''
		orders = Order.select().join(Status).where(Status.status_name == Status.STATUS_LIST[-1][1])
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
					Количество: {order.count}
					Статус: {order.status.status_name}
					Комментарий: {order.comment}
					Адрес доставки: {order.location}
					Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
					\n{"":=<25}\n\n
				'''
		await message.answer(msg, reply_markup=ReplyKeyboardRemove())
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders"], reply_markup=ReplyKeyboardRemove())
	except Exception as ex:
		await message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


# ========================= ВЫВОД ОТМЕНЁННЫХ ЗАЯВОК =============================
@dp.message_handler(text=MENU_COMMANDS["refused_orders"])
async def refused_orders(message: types.Message):
	"""
	Выводит отмененные заявки
	:param message: types.Message
	:return:
	"""
	try:
		msg = ''
		orders = Order.select().where(Order.refuse)
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
						Количество: {order.count}
						Статус: {order.status.status_name}
						Комментарий: {order.comment}
						Адрес доставки: {order.location}
						Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
						\n{"":=<25}\n\n
					'''
		await message.answer(msg, reply_markup=ReplyKeyboardRemove())
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders"], reply_markup=ReplyKeyboardRemove())
	except Exception as ex:
		await message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


# ========================= ИЗМЕНЕНИЕ СТАТУСА ЗАЯВКИ =============================
@dp.message_handler(text=MENU_COMMANDS["change_status"])
async def change_status(message: types.Message):
	try:
		msg = ''
		orders = Order.select().join(Status).where(
			Status.status_name != Status.STATUS_LIST[-1][1] and Order.refuse == False)
		for order in orders:
			msg += f'''{order.id} - {order.product.product_name}
						Количество: {order.count}
						Статус: {order.status.status_name}
						Комментарий: {order.comment}
						Адрес доставки: {order.location}
						Дата изменения: {order.change_date.strftime('%d-%m-%Y, %H:%M')}
						\n{"":=<25}\n\n
					'''
		await message.answer(msg, reply_markup=ReplyKeyboardRemove())
		await message.answer(INFO_LIST["change_edit_order"])
		await ChangeStatus.set_order_id.set()
	except MessageTextIsEmpty:
		await message.answer(WARNING_LIST["not_have_orders"], reply_markup=ReplyKeyboardRemove())
	except Exception as ex:
		await message.answer(ERROR_LIST['general_fail'])
		bot_logger.exception(ex)


@dp.message_handler(state=ChangeStatus.set_order_id)
async def set_status(message: types.Message, state: FSMContext):
	re_num = r'\d+'

	try:
		order_id = re.search(re_num, message.text)
		if not order_id:
			await message.answer(WARNING_LIST["invalid_order_id"])
		elif not int(order_id[0]):
			raise BotExceptions.ZeroCount
		else:
			order = Order.get_by_id(order_id[0])
			await state.update_data(order_id=order_id[0])
			await message.answer(INFO_LIST["change_status"], reply_markup=statuses)
			await ChangeStatus.confirm_status.set()
	except BotExceptions.ZeroCount:
		await message.answer(ERROR_LIST["zero_order"])
	except DoesNotExist:
		await message.answer(WARNING_LIST["invalid_order"])


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
		status_id = Status.get(Status.status_name == data["status"])
		try:
			updated_order = Order.update({Order.status: status_id, Order.change_date: datetime.now()}).where(
				Order.id == data["order_id"]
			)
			updated_order.execute()
			order = Order.get_by_id(data["order_id"])
			user = User().select().join(Client).where(Client.id == order.client).get()
			await bot.send_message(
				user.user_id,
				INFO_LIST["status_changed"].format(order.product.product_name, data["status"])
			)
			await call.message.answer(SUCCESS_LIST["change_success"])
			await state.finish()
		except Exception as ex:
			bot_logger.exception(ex)
			await call.message.answer(ERROR_LIST["fail_changing_status"])
			await state.finish()
	else:
		await call.message.answer(INFO_LIST["change_canceled"])
		await state.finish()
