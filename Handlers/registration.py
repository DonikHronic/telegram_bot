from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re

from Keyboards.inline.callback_datas import user_choice
from commands import COMMANDS_LIST
from loader import bot_logger, dp
from states.registration import Registration
from Models.models import User, Client, Buyer, SecretKey


@dp.callback_query_handler(user_choice.filter(role='client'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='client')
	await call.message.answer(COMMANDS_LIST["set_name"])
	await Registration.first_name.set()


@dp.callback_query_handler(user_choice.filter(role='buyer'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='buyer')
	await call.message.answer(COMMANDS_LIST["set_key"])
	await Registration.secret_key.set()


@dp.message_handler(state=Registration.secret_key)
async def buyer_secret_key(message: types.Message, state: FSMContext):
	secret_key = message.text
	bot_logger.debug(f'Secret key: {secret_key}')
	secret = SecretKey()
	check = secret.check_key(secret_key)
	if check:
		await state.update_data(secret_key=secret_key)
		await message.answer(COMMANDS_LIST["set_name"])
		await Registration.first_name.set()
	else:
		await message.answer(f'{COMMANDS_LIST["fail_key"]}\n{secret_key}')
		await state.finish()


@dp.message_handler(state=Registration.first_name)
async def client_first_name(message: types.Message, state: FSMContext):
	name = message.text
	bot_logger.debug(f'Name: {name}')
	await state.update_data(name=name)
	await message.answer(COMMANDS_LIST["set_surname"])
	await Registration.second_name.set()


@dp.message_handler(state=Registration.second_name)
async def client_surname(message: types.Message, state: FSMContext):
	surname = message.text
	bot_logger.debug(f'Surname: {surname}')
	await state.update_data(surname=surname)
	await message.answer(COMMANDS_LIST["set_patronymic"])
	await Registration.patronymic.set()


@dp.message_handler(state=Registration.patronymic)
async def client_patronymic(message: types.Message, state: FSMContext):
	patronymic = message.text
	bot_logger.debug(f'Patronymic: {patronymic}')
	await state.update_data(patronymic=patronymic)
	await message.answer(COMMANDS_LIST["set_phone"])
	await Registration.number.set()


@dp.message_handler(state=Registration.number)
async def phone_handler(message: types.Message, state: FSMContext):
	phone = message.text
	bot_logger.debug(f'Phone: {phone}')
	await state.update_data(phone=phone)
	await message.answer(COMMANDS_LIST["set_email"])
	await Registration.email.set()


@dp.message_handler(state=Registration.email)
async def email_handler(message: types.Message, state: FSMContext):
	email = message.text
	bot_logger.debug(f'Email: {email}')
	data = await state.get_data()
	user = User()
	user_params = {
		'name': message.from_user.username,
		'id_user': message.from_user.id,
		'email': email,
		'phone': data['phone']
	}

	person_params = {
		'username': message.from_user.username,
		'name': data['name'],
		'surname': data['surname'],
		'patronymic': data['patronymic']
	}

	try:
		user.add_new_user(user_params)

		if data['role'] == 'client':
			client = Client()
			client.add_person(person_params)
		else:
			buyer = Buyer()
			buyer.add_person(person_params)
	except Exception as ex:
		bot_logger.exception(ex)
		await message.answer(COMMANDS_LIST["fail_registration"])
		return

	await state.update_data(email=email)
	await message.answer(f'{COMMANDS_LIST["success_registration"]}!\n{COMMANDS_LIST["show_actions"]}')
	await state.finish()
