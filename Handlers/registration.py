from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
import re

from Keyboards.inline.callback_datas import user_choice
from commands import INFO_LIST, ERROR_LIST, SUCCESS_LIST, WARNING_LIST
from loader import bot_logger, dp
from states.registration import Registration
from Models.models import User, Client, Buyer, SecretKey

re_phone = re.compile(r'^(\+\w{12})$')
re_email = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')


@dp.callback_query_handler(user_choice.filter(role='client'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='client')
	await call.message.answer(INFO_LIST["set_name"])
	await Registration.first_name.set()


@dp.callback_query_handler(user_choice.filter(role='buyer'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='buyer')
	await call.message.answer(INFO_LIST["set_key"])
	await Registration.secret_key.set()


@dp.message_handler(state=Registration.secret_key)
async def buyer_secret_key(message: types.Message, state: FSMContext):
	secret_key = message.text
	bot_logger.debug(f'Secret key: {secret_key}')
	secret = SecretKey()
	check = secret.check_key(secret_key)
	if check:
		await state.update_data(secret_key=secret_key)
		await message.answer(INFO_LIST["set_name"])
		await Registration.first_name.set()
	else:
		await message.answer(f'{ERROR_LIST["fail_key"]}\n{secret_key}')
		await state.finish()


@dp.message_handler(state=Registration.first_name)
async def client_first_name(message: types.Message, state: FSMContext):
	name = message.text
	bot_logger.debug(f'Name: {name}')
	await state.update_data(name=name)
	await message.answer(INFO_LIST["set_surname"])
	await Registration.second_name.set()


@dp.message_handler(state=Registration.second_name)
async def client_surname(message: types.Message, state: FSMContext):
	surname = message.text
	bot_logger.debug(f'Surname: {surname}')
	await state.update_data(surname=surname)
	await message.answer(INFO_LIST["set_phone"])
	await Registration.number.set()


@dp.message_handler(state=Registration.patronymic)
async def client_patronymic(message: types.Message, state: FSMContext):
	patronymic = message.text
	bot_logger.debug(f'Patronymic: {patronymic}')
	await state.update_data(patronymic=patronymic)
	await message.answer(INFO_LIST["set_phone"])
	await Registration.number.set()


@dp.message_handler(state=Registration.number)
async def phone_handler(message: types.Message, state: FSMContext):
	phone = message.text
	bot_logger.debug(f'Phone: {phone}')
	if not re.search(re_phone, phone):
		await message.answer(WARNING_LIST["invalid_number"])
	else:
		data = await state.get_data()
		user = User()
		user_params = {
			'name': message.from_user.username,
			'id_user': message.from_user.id,
			'email': '-',
			'phone': phone
		}

		person_params = {
			'username': message.from_user.username,
			'name': data['name'],
			'surname': data['surname'],
			'patronymic': '-'
		}

		try:
			user.add_new_user(user_params)

			if 'client' in data['role']:
				client = Client()
				client.add_person(person_params)
			else:
				buyer = Buyer()
				buyer.add_person(person_params)
				user = User()
				id_user = user.get(User.user_id == message.from_user.id)
				key = SecretKey.update(buyer=id_user.id).where(SecretKey.key == data['secret_key'])
				key.execute()
		except Exception as ex:
			bot_logger.exception(ex)
			await message.answer(ERROR_LIST["fail_registration"])
			await state.finish()
			return

		await message.answer(f'{SUCCESS_LIST["success_registration"]}!\n{INFO_LIST["show_actions"]}')
		await state.finish()


@dp.message_handler(state=Registration.email)
async def email_handler(message: types.Message, state: FSMContext):
	email = message.text
	bot_logger.debug(f'Email: {email}')
	if not re.match(re_email, email):
		await message.answer(WARNING_LIST["invalid_email"])
	else:
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

			if 'client' in data['role']:
				client = Client()
				client.add_person(person_params)
			else:
				buyer = Buyer()
				buyer.add_person(person_params)
				user = User()
				id_user = user.get(User.user_id == message.from_user.id)
				key = SecretKey.update(buyer=id_user.id).where(SecretKey.key == data['secret_key'])
				key.execute()
		except Exception as ex:
			bot_logger.exception(ex)
			await message.answer(ERROR_LIST["fail_registration"])
			await state.finish()
			return

		await message.answer(f'{SUCCESS_LIST["success_registration"]}!\n{INFO_LIST["show_actions"]}')
		await state.finish()
