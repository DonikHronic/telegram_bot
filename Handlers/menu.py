from aiogram import types
from aiogram.dispatcher.filters import Command

from Keyboards.default.menu import menu_client, menu_buyer
from Models.models import Client, Buyer, User
from commands import INFO_LIST, WARNING_LIST
from loader import dp


@dp.message_handler(Command('menu'))
async def show_menu(message: types.Message):
	id_user = User.get(User.user_id == message.from_user.id)
	buyer = Buyer.select().where(Buyer.user == id_user.id)
	client = Client.select().where(Client.user == id_user.id)

	if buyer.exists():
		await message.answer(INFO_LIST["choose_action"], reply_markup=menu_buyer)
	elif client.exists():
		await message.answer(INFO_LIST["choose_action"], reply_markup=menu_client)
	else:
		await message.answer(WARNING_LIST["not_registered"])
