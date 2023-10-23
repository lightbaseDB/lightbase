from typing import Any, AnyStr

from pymongo import MongoClient
from redis import Redis

class Connection:
    """
    Connection class is responsible for connecting to the database and cache system.

    Attributes:
        mongo_client (MongoClient): MongoClient instance.
        redis_client (Redis): Redis instance.
        DataBase (Any): The database to connect to.
    """


    def __init__( self, mongo_uri: Any | str, redis_uri: Any | str, DataBase: str ) -> Any:
        self.__mongo_client = MongoClient()
        self.__redis_client = Redis().from_url(redis_uri)
        self.__db = DataBase


    def __get_mongo_client__( self ) -> MongoClient:
        return self.__mongo_client
    
    def __get_redis_client__( self ) -> Redis:
        return self.__redis_client
    
    def __get_mongo_db__( self ) -> Any:
        return self.__get_mongo_client__()[self.__db]
    
    def set( self, key: str, value: str | dict, ttl: int ) -> Any:
        """
        Sets data into the DB and cache.
        """

        value = self.___format_value(value)

        result = self.__get_redis_client__().get(key)

        if result is None or not result:
            self.__get_redis_client__().set(
                key,
                value,
                ttl
            )

            self.__get_mongo_db__().insert_one(value)

            return value

    def ___format_value(value):
        """
        Formats the value as a string with single quotes around the keys if it is a dictionary.

        Args:
            value (Any): The value to format.

        Returns:
            str: The formatted value.
        """
        if isinstance(value, dict):
            return str({f"'{k}'": v for k, v in value.items()})
        else:
            return value

