#!/bin/python3
from lib.requests import user_get, order_create, user_orders_get, shop_inventory_get
from aiohttp import web

server = web.Application()
server.add_routes([web.get('/user/get', user_get)])
server.add_routes([web.post('/order/create', order_create)])
server.add_routes([web.get('/user/orders/get', user_orders_get)])
server.add_routes([web.get('/shop/inventory/get', shop_inventory_get)])

web.run_app(server)
