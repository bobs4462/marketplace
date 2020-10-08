#!/bin/python3
from lib import checks

# Making sure that python versin satisfies the requirments (> 3.5) 
checks.version_check()

from lib.handlers import user_get, order_create, user_orders_get, shop_inventory_get
from aiohttp import web

# Creating server instance
server = web.Application()
# Adding handlers for api method calls
server.add_routes([web.get('/user/get', user_get)])
server.add_routes([web.post('/order/create', order_create)])
server.add_routes([web.get('/user/orders/get', user_orders_get)])
server.add_routes([web.get('/shop/inventory/get', shop_inventory_get)])

# Launching server
web.run_app(server)
