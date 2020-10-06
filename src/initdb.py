from tables import BASE
from db import DB

db = DB('marketplace.db')

BASE.metadata.create_all(db.get_engine())
