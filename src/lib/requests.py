from aiohttp import web
from datetime import datetime
from sqlalchemy import func
import json
from lib.helpers import validate_int, ValidationStatus, validate_json
from lib.db import DB
from lib.tables import Order, OrderItem, User, Shop, Book, Lot
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING)

db = DB(url="data/marketplace.db")

# Retrieve user information
async def user_get(request: web.Request) -> web.Response:
    response = None
    user_id = request.query['id']
    logging.warning(f'Method /user/get\nParams: user_id: {user_id}')

    # Perform some validation
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating user_id: {status}')
        response = web.Response(
            status=400, body=f'User\'s identificator {status.value}')

    if response is None:
        # Getting session for database interaction
        session = db.get_session()
        # Retrieving record for requested user
        user = session.query(User).filter_by(id=user_id).first()
        # Converting to data json
        user = user.json_serialize()
        response = web.Response(status=200, body=user,
                                content_type='application/json')
    
    return response

# Create order, with particular book and it's quantity


async def order_create(request: web.Request) -> web.Response:
    response = None
    content = await request.content.read()
    logging.warning(f'Method /order/create\nParams: {content}')
    status = validate_json(content)
    # Validating correct JSON
    if status != ValidationStatus.OK:
        logging.error(f'Error validating params: {status}')
        response = web.Response(
            status=400, body=f'Order information {status.value}')
    # getting body of request in dict
    content = json.loads(content)

    # Let's perform some further validity checks first
    book_id = content.get('book_id')
    status = validate_int(book_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating book_id: {status}')
        response = web.Response(
            status=400, body=f'Book\'s identificator {status.value}')
    user_id = content.get('user_id')
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating user_id: {status}')
        response = web.Response(
            status=400, body=f'User\'s identificator {status.value}')
    book_quantity = content.get('book_quantity')
    status = validate_int(book_quantity)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating book_quantity: {status}')
        response = web.Response(
            status=400, body=f'Book\'s quantity {status.value}')
    shop_id = content.get('shop_id')
    status = validate_int(shop_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating shop_id: {status}')
        response = web.Response(
            status=400, body=f'Shop\'s identificator {status.value}')

    # Creating order (from chaos :])
    if response is None:
        session = db.get_session()
        order = Order(user_id=user_id, reg_date=datetime.now())
        # Adding order itself
        session.add(order)
        # Making changes persistent to database
        session.flush()
        # Adding items to above created order
        order_item = OrderItem(
            order_id=order.id, book_id=book_id, book_quantity=book_quantity, shop_id=shop_id)
        session.add(order_item)

        # Commiting changes to database
        session.commit()

        response = web.Response(status=200, body=f'Order {order.id} added')

    return response

# Retrieve order of requested user


async def user_orders_get(request: web.Request) -> web.Response:
    response = None
    user_id = request.query['user_id']
    logging.warning(f'Method /user/orders/get\nParams: user_id: {user_id}')
    # Perform some validation
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating user_id: {status}')
        response = web.Response(
            status=400, body=f'User\'s identificator {status.value}')

    if response is None:
        session = db.get_session()
        # using some crazy amounts of inner joins and filtering out neccessary orders
        records = session.query(Order, Book, OrderItem, Shop).filter(User.id == Order.user_id).filter(
            Order.id == OrderItem.order_id).filter(OrderItem.shop_id == Shop.id).filter(Book.id == OrderItem.book_id).filter(User.id == user_id).all()
        orders = list()
        # put all retrieved data into dict for further convertion into json
        for o, b, i, s in records:
            # could have used more conventinal field names, but for the goals of this project more human readable names will do
            orders.append({
                "Order ID": o.id,
                "Book ID": b.id,
                "Book name": b.name,
                "Book quantity": i.book_quantity,
                "Date of purchase": datetime.strftime(o.reg_date, '%d.%m.%Y %H:%M'),
                "Shop": s.name,
                "Shop's address": s.address
            })

        response = web.Response(status=200, body=json.dumps(orders))
    return response

# Retrieve books in a particular shop and their corresponding numbers


async def shop_inventory_get(request: web.Request) -> web.Response:
    response = None
    shop_id = request.query['shop_id']
    logging.warning(f'Method /shop/inventory/get\nParams: shop_id: {shop_id}')

    status = validate_int(shop_id)
    if status != ValidationStatus.OK:
        logging.error(f'Error validating shop_id: {status}')
        response = web.Response(
            status=400, body=f'Shop\'s identificator {status.value}')
    if response is None:
        session = db.get_session()
        records = session.query(func.count(Book.id).label('count'), Book.name, Book.author).filter(Shop.id == Lot.shop_id).filter(
            Lot.book_id == Book.id).filter(Shop.id == shop_id).group_by(Book.name, Book.author).all()
        books = list()
        for b in records:
            books.append({
                "Book count": b.count,
                "Book name": b.name,
                "Book author": b.author
            })
        response = web.Response(status=200, body=json.dumps(books))
    return response
