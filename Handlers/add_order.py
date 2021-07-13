from aiogram import types
from aiogram.dispatcher import FSMContext

from Models.models import Product
from commands import INFO_LIST, WARNING_LIST
from loader import dp
from states.make_order import MakeOrder


@dp.message_handler(state=MakeOrder.choose_product)
async def choose_product(message: types.Message, state: FSMContext):
	data = await state.get_data()
	try:
		number = int(message.text)
		if number <= data['products_count']:
			product = Product.get(Product.id == number)
			await state.update_data(product_name=product.product_name)
			await message.answer(INFO_LIST["selected_product"].format(product.product_name))
		else:
			await message.answer(WARNING_LIST["invalid_product"])
	except ValueError:
		await state.update_data(product_name=message.text)
		await message.answer(INFO_LIST["product_added"])
		await MakeOrder.search_product.set()


@dp.message_handler(state=MakeOrder.search_product)
async def search_product():
	pass
