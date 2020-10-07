#! /bin/python3
import checks

checks.version_check()

from tables import BASE
import json
from db import DB

db = DB(url='marketplace.db')

BASE.metadata.create_all(db.get_engine())

session = db.get_session()

records = open('data/records.json') 

# Loading data from file into a dictionary
records = json.loads(records.read()) 

# Adding User records
from tables import User
users = records['users']

for u in users:
    user = User(id=u['id'], name=u.get('name'), surname=u.get('surname'), patronymic=u.get('patronymic'), email=u['email'])
    session.add(user) # adding record to table

# Adding Book records
from tables import Book
books = records['books']
for b in books:
    book = Book(id=b['id'], name=b.get('name'), author=b.get('author'), isbn=b.get('isbn'))
    session.add(book)

# Adding Shop records
from tables import Shop
shops = records['shops']
for s in shops:
    shop = Shop(id=s['id'], name=s.get('name'), address=s.get('address'), zipcode=s.get('zipcode'))
    session.add(shop)

# Adding Order records
from tables import Order
from datetime import datetime as dt
orders = records['orders']
for o in orders:
    order = Order(id=o['id'], reg_date=dt.strptime(o.get('reg_date'), '%Y-%m-%dT%H:%M'), user_id=o['user_id'])
    session.add(order)

# Adding OrderItem records
from tables import OrderItem
items = records['order_items']
for i in items:
    item = OrderItem(id=i['id'], order_id=i['order_id'], book_id=i['book_id'], shop_id=i['shop_id'], book_quantity=i['book_quantity'])
    session.add(item)

# Adding Lot records, not in assignment, but otherwise not possible to complete part 2 of the that assignment
from tables import Lot
lots = records['lots']
for l in lots:
    lot = Lot(id=l['id'], shop_id=l['shop_id'], book_id=l['book_id'])
    session.add(lot)


# Committing changes to database and closing connection
session.commit()
