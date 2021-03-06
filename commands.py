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
	'choose_product': '''
		Введите номер продута который хотите выбрать.
		
		Если не нашли то что нужно,
		можете ввести название продукта и поискать
	''',
	'selected_product': 'Вы выбрали продукт: {0}',
	'product_not_exist': '''
		Мы не нашли продукт который вам нужен. Вы можете указать название товара дальше в коментарии к заявке
	''',
	'search_in_progress': 'Поиск похожих продуктов',
	'set_count': 'Укажите количество',
	'set_limit': 'Установите крайний срок выполнения заявки',
	'deadline_set': 'Срок установлен',
	'set_location': 'Введите адрес доставки',
	'add_comment': '''
		Добваьте описание к продукту который вы выбрали ранее.
		Также можете написать название продукта если не указали его выше
	''',
	'confirm': 'Подтвердить получение',
	'confirmed': 'Заявка завершена',
	'check_confirm': 'В точно получили товар?',
	'set_order_id': 'Укажите номер заявки которую хотите отменить',
	'refuse_decline': 'Отмена заявки прервана',
	'refused': 'Заявка продукт {0}, в количестве {1} отменена',
	'show_all_orders': 'Показать все заявки',
	'show_complete_orders': 'Показать завершенные заявки',
	'show_new_orders': 'Показать новые завки',
	'show_orders_btn': 'Вы можете выбрать как вывести список завок',
	'choose_showing': 'Выберите один вариант из представленных',
	'change_status': 'Выберите статус на который хотите поменять',
	'change_edit_order': 'Выберите номер продукта статус которого хотите поменять',
	'confirm_status': 'Вы уверены?\nНовый статус: {0}',
	'change_canceled': 'Изменение статуса отменено',
	'empty_orders': 'Продуктов нет',
	'status_changed': 'Статус вашей заявки на {0}, изменен на {1}',
	'request_completed': 'Заявки на {0} завершена, клиент принял заказ.\nВремя завершения: {1}',
	'new_order': 'Добавлена новая заявка',
}

SUCCESS_LIST = {
	'success_registration': 'Регистрация завершена',
	'order_added': 'Ваша заявка принята. Вы сможете просматривать статус выполнения заявки в пункте Меню -> Мои заявки',
	'change_success': 'Статус изменен'
}

WARNING_LIST = {
	'not_registered': 'Вы не зарегистрированы. Можете зарегистрироваться командой /start',
	'invalid_number': '''
		Неверно введён номер телефона! Номер телефона должен начинаться с + и содержать 12 цифр.
		Пример: +998991234567
	''',
	'invalid_email': 'Данный Email адрес некорректный. Попробуйте заново. Пример: example@example.example',
	'invalid_product': 'Вы ввели неверный номер продукта',
	'not_confirmed': 'После того как получите товар, подтвердите получение',
	'not_have_orders_refuse': 'У вас нет заявок которые можно отменить',
	'invalid_order_id': 'Номер заявки должен состоять из цифр',
	'invalid_order': 'Заявки с таким номером у вас не существует',
	'check_refusing': 'Вы точно хотите отменить заявку?',
	'not_have_orders': 'Пока не имеется заявок'
}

ERROR_LIST = {
	'fail_registration': 'При регистрации возникла ошибка. Пожалуйта попробуйте снова',
	'fail_key': 'Ключ неверный. Обратитесь к администратору',
	'fail_count': 'Количество надо ввести цифрами',
	'order_adding_fail': 'При добавлении заявки произошла ошибка. Пожалуйста повторите попытку',
	'fail_show_orders': 'При выводе ваших заявок произошла ошибка. Пожалуйста повторите попытку',
	'refuse_order': 'При выводе ваших заявок для отмены произошла ошибка. Пожалуйста повторите попытку',
	'fail_changing_status': 'При изменении статуса произошла ошибка. Пожалуйста повторите попытку',
	'zero_count': 'Нулевое количество продукта недопустимо',
	'zero_order': 'Нулевая завка недопустима',
	'general_fail': 'Что то пошло не так. Попробуйте пожлуста позже',
}

MENU_COMMANDS = {
	'add_order': 'Добавить заявку',
	'my_orders': 'Мои заявки',
	'refuse_order': 'Отмена заявки',
	'connect_buyer': 'Связь с закупщиком',
	'show_orders_btn': 'Вывод заявок',
	'orders_history': 'История заявок',
	'change_status': 'Изменение статуса заявки',
	'refused_orders': 'Отмененные заявки',
}
