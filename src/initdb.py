#!/bin/python3
from datetime import datetime as dt
from lib.tables import Order, Shop, Book, User, OrderItem, Lot, BASE
from lib.db import DB
import json
from lib import checks

checks.version_check()


db = DB(url='data/marketplace.db')

BASE.metadata.create_all(db.get_engine())

session = db.get_session()

records = open('data/records.json')

# Loading data from file into a dictionary
records = json.loads(records.read())

# Adding User records
users = records['users']

for u in users:
    user = User(id=u['id'], name=u.get('name'), surname=u.get(
        'surname'), patronymic=u.get('patronymic'), email=u['email'])
    session.add(user)  # adding record to table

# Adding Book records
books = records['books']
for b in books:
    book = Book(id=b['id'], name=b.get('name'),
                author=b.get('author'), isbn=b.get('isbn'))
    session.add(book)

# Adding Shop records
shops = records['shops']
for s in shops:
    shop = Shop(id=s['id'], name=s.get('name'), address=s.get(
        'address'), zipcode=s.get('zipcode'))
    session.add(shop)

# Adding Order records
orders = records['orders']
for o in orders:
    order = Order(id=o['id'], reg_date=dt.strptime(
        o.get('reg_date'), '%Y-%m-%dT%H:%M'), user_id=o['user_id'])
    session.add(order)

# Adding OrderItem records
items = records['order_items']
for i in items:
    item = OrderItem(id=i['id'], order_id=i['order_id'], book_id=i['book_id'],
                     shop_id=i['shop_id'], book_quantity=i['book_quantity'])
    session.add(item)

# Adding Lot records, not in assignment, but otherwise not possible to complete part 2 of the that assignment
lots = records['lots']
for l in lots:
    lot = Lot(id=l['id'], shop_id=l['shop_id'], book_id=l['book_id'])
    session.add(lot)


# Committing changes to database and closing connection
session.commit()
