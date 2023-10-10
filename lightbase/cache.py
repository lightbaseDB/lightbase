from __future__ import annotations

from typing import Any, Dict

from cache3 import Cache as cs

from lightbase.crypto import Crypto


class Cache:
    """
    Cache Class

    ---

    This class is used to store the cache data.

    Attributes:
    -----------
    cache: Dict[str, Any]
        The cache data.

    Methods:
    --------

    get(key: str) -> Any
        Get the value of the key in the cache.

    set(key: str, value: Any) -> None

    delete(key: str) -> None
        Delete the key in the cache.

    clear() -> None
        Clear the cache.
    """

    def __init__(
            self,
            #cache: Dict[str, Any] = None
    ) -> None:
        """
        Parameters:
        -----------

        cache: Dict[str, Any]
            The cache data.
        """
        self.cache = "test"

    def set(self, key, value):
        cs.set(key=key, value=value, timeout=60)

    def get(self, key):
        cs.get(key)


cache.set(key="test", value={"test": 2467})

print(cache.get("test"))