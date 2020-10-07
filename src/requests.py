from aiohttp import web
from helpers import validate_int, ValidationStatus
from db import DB

db = DB(url="marketplace.db")

async def user(request: web.Request) -> web.Response:
    response = None
    user_id = request.query['id']

    # Perform some validation
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'User\'s identificator {status}')

    if not response:
        session = db.get_session()
        from tables import User
        user = session.query(User).filter_by(id=user_id).first()
        user = user.json_serialize()
        response = web.Response(body=user, content_type='application/json')
    return response

async def order_add(request: web.Request) -> web.Response:
    response = None

    # Let's perform some validity checks first
    book_id = request.query['book_id']
    status = validate_int(book_id)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'Book\'s identificator {status}')
    user_id = request.query['book_id']
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'User\'s identificator {status}')
    book_quantity = request.query['book_quantity']
    status = validate_int(book_quantity)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'Book\'s quantity {status}')

    shop_id = request.query['book_quantity']
    status = validate_int(book_quantity)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'Book\'s quantity {status}')

    # Creating order (from chaos :])
    from tables import Order, OrderItem
    from datetime import datetime
    session = db.get_session()
    order = Order(user_id=user_id, reg_date=datetime.now())
    session.add(order)
    session.flush()
    order_item = OrderItem(order_id=order.id, book_id=book_id, book_quantity=book_quantity, shop_id=shop_id)
    session.commit()

    response = web.Response(status=200, reason=f'OK, order {order.id} added')


async def user_orders_get(request: web.Request) -> web.Response:
    response = None
    user_id = request.query['id']
    # Perform some validation
    status = validate_int(user_id)
    if status != ValidationStatus.OK:
        response = web.Response(status=400, reason=f'User\'s identificator {status}')

    if not response:
        pass



server = web.Application()
server.add_routes([web.get('/', user)])

web.run_app(server)
