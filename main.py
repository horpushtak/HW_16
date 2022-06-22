from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from classes import User, Offer, Order

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///profi_ru.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        user_data = User.query.all()
        return jsonify([user.user_in_dict() for user in user_data])
    if request.method == 'POST':
        try:
            user = json.loads(request.data)  # Вот эту строчку я не до конца понимаю, мы считываем то, что падает
            # от пользователя, но механику я забыл, повторить json.loads
            new_user = User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
            with db.session.begin:
                db.session.add(new_user)
                db.session.commit()
                return "Пользователь создан в базе данных", 200  # Коды нам понадобятся потом
        except Exception as e:
            return e


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user_by_id(user_id):
    if request.method == 'GET':
        user = db.session.query(User).get(user_id)
        if user == None:
            return "Пользователь не найден", 404
        else:
            return jsonify(user.user_in_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user == None:
            return "Пользователь не найден", 404
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]
        with db.session.begin():
            db.session.add(user)
            db.session.commit()
        return f"Пользователь с id {user_id} добавлен", 200
    elif request.method == "DELETE":
        user = db.session.query(User).get(user_id)
        if user == None:
            return "Пользователь не найден", 404
        with db.session.begin():
            db.session.delete(user)
            db.session.commit()
        return f"Пользователь с id {user_id} удалён", 200


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        order_data = Order.query.all()
        return jsonify([order.order_in_dict() for order in order_data])
    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            new_order = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=order['start_date'],
                end_date=order['end_date'],
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            with db.session.begin:
                db.session.add(new_order)
                db.session.commit()
                return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def get_order_by_id(order_id):
    if request.method == 'GET':
        order = db.session.query(Order).get(order_id)
        if order == None:
            return "Заказ не найден"
        else:
            return jsonify(order.order_in_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        if order == None:
            return "Заказ не найден", 404
        order.id = order_data['id'],
        order.name = order_data['name'],
        order.description = order_data['description'],
        order.start_date = order_data['start_date'],
        order.end_date = order_data['end_date'],
        order.address = order_data['address'],
        order.price = order_data['price'],
        order.customer_id = order_data['customer_id'],
        order.executor_id = order_data['executor_id']
        with db.session.begin():
            db.session.add(order)
            db.session.commit()
        return f"Заказ с id {order_id} добавлен", 200
    elif request.method == "DELETE":
        order = db.session.query(Order).get(order_id)
        if order == None:
            return "Заказ не найден", 404
        with db.session.begin():
            db.session.delete(order)
            db.session.commit()
        return f"Заказ с id {order_id} удалён", 200


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        offer_data = Offer.query.all()
        return jsonify([offer.offer_in_dict() for offer in offer_data])
    if request.method == 'POST':
        try:
            offer = json.loads(request.data)
            new_offer = Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
            with db.session.begin:
                db.session.add(new_offer)
                db.session.commit()
                return "Предложение создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def get_offer_by_id(offer_id):
    if request.method == 'GET':
        offer = db.session.query(Order).get(offer_id)
        if offer == None:
            return "Предложение не найдено", 404
        else:
            return jsonify(offer.offer_in_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        if offer == None:
            return "Предложение не найдено", 404
        offer.id = offer_data['id'],
        offer.order_id = offer_data['order_id'],
        offer.executor_id = offer_data['executor_id']
        with db.session.begin():
            db.session.add(offer)
            db.session.commit()
        return f"Предложение с id {offer_id} добавлен", 200
    elif request.method == "DELETE":
        offer = db.session.query(Offer).get(offer_id)
        if offer == None:
            return "Предложение не найдено", 404
        with db.session.begin():
            db.session.delete(offer)
            db.session.commit()
        return f"Предложение с id {offer_id} удалено", 200


if __name__ == "__main__":
    app.run()
