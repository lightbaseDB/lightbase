import os
import sys

from typing import Any

from .connection import Connection

class LightBase:
    """
    LightBase class is responsible for managing the database and cache system.

    Attributes:
        __connection (Connection): Connection instance.
    """
    

    def __init__( self, mongo_uri: str, redis_uri: str, ttl: int = 60 ) -> None:
        self.__connection = Connection(mongo_uri, redis_uri)
        self.__ttl = ttl

    
    def set( self, key: str, value: str | dict) -> Any:
        """
        Sets data into the DB and cache.
        """

        self.___format_value(value)
