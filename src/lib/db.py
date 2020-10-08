from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
    # class constructor, would be nice to make it more database agnostic
    def __init__(self, driver: str = 'sqlite', url: str=''):
        self.__url = url
        self.__engine = create_engine(f'{driver}:///{url}')
        Session = sessionmaker()
        Session.configure(bind=self.__engine)
        self.__session_class = Session
    # Accessor for engine object (unified interface to underlying database), which is used elsewhere in framework
    def get_engine(self):
        return self.__engine

    # Accessor for session object, which is used for direct communication with the database, sort of a handle for current connection
    def get_session(self):
        return self.__session_class()

from sqlalchemy.engine import Engine
from sqlalchemy import event

# https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys 
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
