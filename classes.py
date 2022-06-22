from main import db  # отдельно забираем сюда, (как вот это назвать?), объект связи между базой и приложением
import datetime
import data

"""Нужно прописать поля моделей"""
"""Упаковка в словарик ручная, в 17 уроке бодрее дело идёт, можно потом здесь всё переделать"""


class User(db.Model):
    __tablename__ = "user"  # foreign key будет ссылаться сюда, так связываются именно таблицы (?)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(250))
    phone = db.Column(db.String(100))

    def user_in_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)  # Тут сколько угодно можно написать, поэтому не String,
    # хотя в чём разница между ними до конца не ясно
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(250))
    price = db.Column(db.Float)  # Здесь вроде бы не должен быть int
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # Из таблицы user берём id, как поле класса
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def order_in_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def offer_in_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


db.create_all()

"""Теперь нужно занести данные в базу"""
for user in data.USERS:
    with db.session.begin():  # with сам коммитит или нужно отдельно прописывать?
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        ))
        db.session.commit()

for order in data.ORDERS:
    month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
    # Тут понятно что и как расковыряли, но почему сначала задаём переменную, а потом используем её после for
    # до конца неясно. Погуглить. Ощущение, что она должна создаваться в момент использования, после for
    month_end, day_end, year_end = [int(_) for _ in order['end_date'].split("/")]
    with db.session.begin():
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=year_start, month=month_start, day=day_start),
            end_date=datetime.date(year=year_end, month=month_end, day=day_end),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))
        db.session.commit()

for offer in data.OFFERS:
    with db.session.begin():
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))
        db.session.commit()
