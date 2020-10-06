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
