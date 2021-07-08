from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from Keyboards.inline.callback_datas import user_choice
from loader import bot_logger, dp
from states.registration import Registration


@dp.callback_query_handler(user_choice.filter(role='client'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='client')
	await call.message.answer('Регистрация клиента!\nВведите свое имя!')
	await Registration.first_name.set()


@dp.callback_query_handler(user_choice.filter(role='buyer'), state=None)
async def add_new_client(call: CallbackQuery, state: FSMContext):
	await call.answer(cache_time=60)
	await state.update_data(role='buyer')
	await call.message.answer('Регистрация закупщика!\nВведите свое имя!')
	await Registration.first_name.set()


@dp.message_handler(state=Registration.first_name)
async def client_first_name(message: types.Message, state: FSMContext):
	name = message.text
	bot_logger.debug(f'Name: {name}')
	await state.update_data(name=name)
	await message.answer('Введите фамилию!')
	await Registration.second_name.set()


@dp.message_handler(state=Registration.second_name)
async def client_surname(message: types.Message, state: FSMContext):
	surname = message.text
	bot_logger.debug(f'Surname: {surname}')
	await state.update_data(surname=surname)
	await message.answer('Введите отчество!')
	await Registration.patronymic.set()


@dp.message_handler(state=Registration.patronymic)
async def client_patronymic(message: types.Message, state: FSMContext):
	patronymic = message.text
	bot_logger.debug(f'Patronymic: {patronymic}')
	await state.update_data(patronymic=patronymic)
	await message.answer('Введите Email!')
	await Registration.email.set()


@dp.message_handler(state=Registration.email)
async def email_handler(message: types.Message, state: FSMContext):
	email = message.text
	bot_logger.debug(f'Email: {email}')
	name = await state.get_data()
	await state.update_data(email=email)
	await message.answer('Регистрация завершена!')
	await state.finish()
