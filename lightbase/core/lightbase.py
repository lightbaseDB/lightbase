from typing import Any

from .connection import Connection

class LightBase:
    """
    LightBase class is responsible for managing the database and cache system.

    Attributes:
        mongo_uri (str): MongoDB URI.
        redis_uri (str): Redis URI.
        ttl (int): Time to live in seconds.
    """
    

    def __init__( self, mongo_uri: str, redis_uri: str, ttl: int = 60 ) -> None:
        self.__connection = Connection(mongo_uri, redis_uri)
        self.__ttl = ttl

    def __get_connection__( self ) -> Connection:
        return self.__connection
    
    def __get_ttl__( self ) -> int:
        return self.__ttl
    
    def set( self, key: str, value: str | dict) -> Any:
        """
        Sets data into the DB and cache.
        """

        return self.__get_connection__().set(key, value, self.__get_ttl__())
    
    def get( self, key: str ) -> Any:
        """
        Gets data from the DB or cache.
        """

        return self.__get_connection__().get(key)
    
    def delete( self, key: str ) -> Any:
        """
        Deletes data from the DB and cache.
        """

        return self.__get_connection__().delete(key)
    
    def update( self, key: str, value: str | dict ) -> Any:
        """
        Updates data from the DB and cache.
        """

        return self.__get_connection__().update(key, value, self.__get_ttl__())
    
    def exists( self, key: str ) -> bool:
        """
        Checks if data exists in the DB or cache.
        """

        return self.__get_connection__().exists(key)
    
    def clear( self, asynchronous: bool ) -> bool:
        """
        Clears the DB and cache.
        """

        return self.__get_connection__().clear(asynchronous=asynchronous)
    
    def close( self ) -> bool:
        """
        Closes the DB and cache.
        """

        return self.__get_connection__().close()
    
    def __repr__( self ) -> str:
        return f'<LightBase mongo_uri={self.mongo_uri} redis_uri={self.redis_uri} ttl={self.ttl}>'
    
    def __str__( self ) -> str:
        return f'<LightBase mongo_uri={self.mongo_uri} redis_uri={self.redis_uri} ttl={self.ttl}>'
    
    def __del__( self ) -> None:
        self.__get_connection__().close()
        del self.__connection
        del self.__ttl