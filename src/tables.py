from sqlalchemy.ext import declarative
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

# base class, sqlalchemy magic
BASE = declarative.declarative_base()

# All classed that are mapped to real database tables inherit from the base class,
# sqlalchemy will then be able to describe database schema and map our classes accordingly.

class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    email = Column(String)

class Book(BASE):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    isbn = Column(String)

class Shop(BASE):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    zipcode = Column(String)

class Order(BASE):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    reg_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

class OrderItem(BASE):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    book_quantity = Column(Integer)
    shop_id = Column(Integer, ForeignKey('shop.id'))
