from aiohttp import web
from db import DB

db = DB(url="marketplace.db")

async def user(request: web.Request) -> web.Response:
    user_id = request.query['id']
    response = None
    # checking for absent user_id in request
    if not user_id:
        response = web.Response(status=400, reason='User\'s identificator is missing')
    # let's check that requested id is a valid integer
    try:
        user_id = int(user_id)
    except ValueError:
        response = web.Response(status=400, reason='User\'s identificator is not a number')
    session = db.get_session()

    from tables import User
    user = session.query(User).filter_by(id=user_id).first()
        
    print(user)
    return response


server = web.Application()
server.add_routes([web.get('/', user)])

web.run_app(server)
