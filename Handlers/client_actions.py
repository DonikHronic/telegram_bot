import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from Models.models import Product
from commands import MENU_COMMANDS, INFO_LIST
from loader import dp
from states.make_order import MakeOrder


@dp.message_handler(text=MENU_COMMANDS["add_order"])
async def add_order(message: types.Message, state: FSMContext):
	items = Product.select()
	msg = ''
	for item in items:
		msg += f'{item.id} - {item.product_name}\n'

	products_count = len(msg.split('\n')) - 1
	await state.update_data(products_count=products_count)
	await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
	await message.answer(INFO_LIST["choose_product"])
	await MakeOrder.choose_product.set()


@dp.message_handler(text=MENU_COMMANDS["my_orders"])
async def my_orders(message: types.Message):
	await message.answer('List', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["refuse_order"])
async def refuse_order(message: types.Message):
	await message.answer('List', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text=MENU_COMMANDS["connect_buyer"])
async def connect_buyer(message: types.Message):
	await message.answer('@username', reply_markup=types.ReplyKeyboardRemove())
