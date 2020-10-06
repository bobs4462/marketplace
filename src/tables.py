from sqlalchemy.ext import declarative
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime
from helpers import Serializable

# base class, sqlalchemy magic
BASE = declarative.declarative_base()

# All classes that are mapped to real database tables inherit from the base class,
# sqlalchemy will then be able to describe database schema and map our classes accordingly.

class User(BASE, Serializable):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    patronymic = Column(String)
    email = Column(String, nullable=False, unique=True)
    def serialize(self) -> dict:
        return { "name": self.name,
                "surname": self.patronymic,
                "patronymic": self.patronymic,
                "email": self.email }

class Book(BASE, Serializable):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    isbn = Column(String, unique=True)

class Shop(BASE, Serializable):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    zipcode = Column(String)

class Order(BASE, Serializable):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    reg_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class OrderItem(BASE, Serializable):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    book_quantity = Column(Integer, nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.id'), nullable=False)

