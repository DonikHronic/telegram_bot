INFO_LIST = {
	'bot_started': 'Бот Запущен.',
	'start': 'Приветствую в боте.',
	'registration': 'Регистрация',
	'exist_registration': 'Вы уже зарегистрированы в системе',
	'show_actions': 'Можете просмотреть действия командой /menu',
	'choose_action': 'Выберите действие которое хотите выплонить',
	'set_name': 'Введите имя!',
	'set_surname': 'Введите фамилию',
	'set_patronymic': 'Введите отчество',
	'set_email': 'Введите email',
	'set_phone': 'Введите номер телефона',
	'set_key': 'Введите секретный ключ',
	'registration_client': 'Регистрация клиента',
	'client': 'Я клиент',
	'buyer': 'Я закупщик',
	'products': '',
	'choose_product': '''
		Введите номер продута который хотите выбрать.\n\nЕсли не нашли то что нужно,
		можете ввести название продукта и поискать
	''',
	'selected_product': 'Вы выбрали продукт: {0}',
}

SUCCESS_LIST = {
	'success_registration': 'Регистрация завершена',

}

WARNING_LIST = {
	'not_registered': 'Вы не зарегистрированы. Можете зарегистрироваться командой /start',
	'invalid_number': '''
		Неверно введён номер телефона! Номер телефона должен начинаться с + и содержать 12 цифр.
		Пример: +998991234567
	''',
	'invalid_email': 'Данный Email адрес некорректный. Попробуйте заново. Пример: example@example.example',
	'invalid_product': 'Вы ввели неверный номер продукта',
}

ERROR_LIST = {
	'fail_registration': 'При регистрации возникла ошибка. Пожалуйта попробуйте снова',
	'fail_key': 'Ключ неверный. Обратитесь к администратору',
}

MENU_COMMANDS = {
	'add_order': 'Добавить заявку',
	'my_orders': 'Мои заявки',
	'refuse_order': 'Отмена заявки',
	'connect_buyer': 'Связь с закупщиком',
	'show_orders': 'Вывод заявок',
	'orders_history': 'История заявок',
	'change_status': 'Изменение статуса заявки',
	'refused_orders': 'Отмененные заявки',
}
