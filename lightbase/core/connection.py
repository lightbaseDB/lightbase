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


    def __init__( self, mongo_uri: Any | str, redis_uri: Any | str, DataBase: str = "test", Colletion: str = "fs" ) -> Any:
        self.__mongo_client = MongoClient()
        self.__redis_client = Redis().from_url(redis_uri)
        self.__db = DataBase
        self.__col = Colletion


    def __get_mongo_client__( self ) -> MongoClient:
        return self.__mongo_client
    
    def __get_redis_client__( self ) -> Redis:
        return self.__redis_client
    
    def __get_mongo_db__( self ) -> Any:
        return self.__get_mongo_client__()[self.__db]
    
    def __get_mongo_col__( self ) -> Any:
        return self.__get_mongo_db__()[self.__col]
    
    def set( self, key: str, value: str | dict, ttl: int ) -> Any:
        """
        Sets data into the DB and cache.
        """

        value = self.___format_value(value=value)


        result = self.__get_redis_client__().get(key)

        if result is None or not result:
            self.__get_redis_client__().set(
                key,
                value,
                ttl
            )

            self.__get_mongo_col__().insert_one(
                {
                    key: value
                }
            )

            return value
        
        else:
            if self.__get_mongo_col__().find_one({key: {'$exists': True}}):
                self.__get_mongo_col__().update_one(
                    {key: {'$exists': True}},
                    {'$set': value}
                )

                return value
            
            else:
                self.__get_mongo_col__().insert_one(
                    {
                        key: value
                    }
                )

                return value
        
    def get( self, key: str ) -> Any:
        """
        Gets data from the DB or cache.
        """

        result = self.__get_redis_client__().get(key)

        if result is None or not result:
            if self.__get_mongo_col__().find_one({key: {'$exists': True}}):
                return self.__get_mongo_col__().find_one({key: {'$exists': True}})[key]
            
            return None
        
        else:
            return result
        
    def delete( self, key: str ) -> Any:
        """
        Deletes data from the DB or cache.
        """

        result = self.__get_redis_client__().delete(key)

        if result is None or not result:
            if self.__get_mongo_col__().find_one({key: {'$exists': True}}):
                self.__get_mongo_col__().delete_one({key: {'$exists': True}})
            
            return None
        
        else:
            return result
        
    def update( self, key: str, value: str | dict, ttl: int ) -> Any:
        """
        Updates data in the DB and cache.
        """

        value = self.___format_value(value)

        result = self.__get_redis_client__().get(key)

        if result is None or not result:
            self.__get_redis_client__().set(
                key,
                value,
                ttl
            )

            self.__get_mongo_col__().update_one(
                {key: {'$exists': True}},
                {'$set': value}
            )

            return value
        
        else:
            self.__get_redis_client__().set(
                key,
                value,
                ttl
            )

            self.__get_mongo_col__().update_one(
                {key: {'$exists': True}},
                {'$set': value}
            )

            return value
        
    def exists( self, key: str ) -> bool:
        """
        Checks if the key exists in the DB or cache.
        """

        result = self.__get_redis_client__().get(key)

        if result is None or not result:
            if self.__get_mongo_col__().find_one({key: {'$exists': True}}):
                return True
            
            return False
        
        else:
            return True
        
    def clear( self, asynchronous: bool ) -> Any:
        """
        Clears the DB and cache.
        """
        try:
            self.__get_redis_client__().flushall(asynchronous=asynchronous)
            self.__get_mongo_col__().drop()
        
        except Exception as e:
            return False and e
        
        return True
    
    def close( self ) -> bool:
        """
        Closes the connection to the DB and cache.
        """

        try:
            self.__get_redis_client__().close()
            self.__get_mongo_client__().close()
        
        except Exception as e:
            return False and e
        
        return True
    def ___format_value(self, value):
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

