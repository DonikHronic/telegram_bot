from datetime import datetime
from peewee import *

db = SqliteDatabase('bot_db.sql')


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
		return pers

	def is_exist(self, user_id):
		user = self.select().where(User.user_id == user_id)
		if user.exists():
			return True
		return False


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
		return person

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

	def add_order(self, params: dict):
		client = Client.get(Client.user.user_id == params['client_id'])
		buyer = Buyer.get(Buyer.id == 1)
		product = Product.get(Product.product_name == params['product_name'] and Product.count == params['count'])
		status = Status.get(Status.status_name == params['status'])
		period = datetime.strptime(params['period'], '%Y-%m-%d')

		self.create(
			client=client.id,
			buyer=buyer.id,
			comment=params['comment'],
			count=params['count'],
			period=period,
			product=product.id,
			status=status.id,
		)


class History(BaseModel):
	order = ForeignKeyField(Order)


class SecretKey(BaseModel):
	key = CharField()
	buyer = ForeignKeyField(Buyer)


if __name__ == '__main__':
	db.create_tables([User, Client, Buyer, Order, Product, Status, History, SecretKey], safe=True)
