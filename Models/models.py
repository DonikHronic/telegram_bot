from peewee import *
from config import DB_PATH
from loader import bot_logger

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	username = CharField()
	user_id = BigIntegerField()
	email = CharField()
	phone_number = CharField()

	def add_new_user(self, params: dict):
		pers = self.create(
			username=params['name'],
			user_id=params['id_user'],
			email=params['email'],
			phone_number=params['phone']
		)
		bot_logger.info(f'Added new user: {params["name"]}')
		return pers

	def is_exist(self, user_id):
		try:
			user = self.select().where(User.user_id == user_id)
			return user.exists()
		except Exception as ex:
			bot_logger.exception(ex)


class Person(BaseModel):
	user = ForeignKeyField(User)
	first_name = CharField()
	second_name = CharField()
	patronymic = CharField()

	def add_person(self, params: dict):
		user = User.get(User.username == params['username'])
		person = self.create(
			user=user.id,
			first_name=params['name'],
			second_name=params['surname'],
			patronymic=params['patronymic']
		)
		bot_logger.info('Register new person')
		return person

	def check_person(self, user_id):
		id_user = User.get(User.user_id == user_id)
		buyers = self.select().where(self.user == id_user.id)

		return buyers.exists()

	class Meta:
		database = db
		abstract = True


class Client(Person):
	pass


class Buyer(Person):
	pass


class Product(BaseModel):
	product_name = CharField()

	def add_product(self, params: dict):
		product = self.create(
			product_name=params['product_name'],
		)
		return product


class Status(BaseModel):
	STATUS_LIST = [
		('accepted', 'Принята'),
		('in_process', 'В процессе'),
		('sent', 'Отправлена'),
		('complete', 'Завершён'),
	]
	status_name = CharField(choices=STATUS_LIST)


class Order(BaseModel):
	client = ForeignKeyField(Client)
	buyer = ForeignKeyField(Buyer)
	comment = CharField()
	count = IntegerField()
	period = DateTimeField()
	product = ForeignKeyField(Product)
	status = ForeignKeyField(Status)
	location = CharField()
	refuse = BooleanField(default=False)

	def add_order(self, params: dict):
		user_id = User.get(User.user_id == params['client_id'])
		client = Client.get(Client.user == user_id)
		buyer = Buyer.get(Buyer.id == 1)
		product = Product.get(Product.id == params['product_id'])
		status = Status.get(Status.status_name == Status.STATUS_LIST[0][1])

		order = self.create(
			client=client.id,
			buyer=buyer.id,
			comment=params['comment'],
			count=params['count'],
			period=params['period'],
			product=product.id,
			status=status,
			location=params['location']
		)

		return order


class History(BaseModel):
	order = ForeignKeyField(Order)


class SecretKey(BaseModel):
	key = CharField()
	buyer = ForeignKeyField(Buyer)

	def check_key(self, key: str):
		secret_key = self.select().where(SecretKey.key == key, SecretKey.buyer == 0)
		return secret_key.exists()


if __name__ == '__main__':
	db.create_tables([User, Client, Buyer, Order, Product, Status, History, SecretKey])
