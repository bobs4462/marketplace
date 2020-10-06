from sqlalchemy import create_engine

class DB:
    # class constructor, would be nice to make it more database agnostic
    def __init__(self, driver: str = 'sqlite', url: str=''):
        self.__url = url
        self.__engine = create_engine(f'{driver}:///{url}')
    # Accessor for engine object (unified interface to underlying database), which is used elsewhere in framework
    def get_engine(self):
        return self.__engine
