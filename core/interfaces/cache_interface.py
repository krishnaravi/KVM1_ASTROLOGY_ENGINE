"""
Abstract interface contract for Caching providers.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class ICacheProvider(ABC):
    """
    Abstract Base Class defining the contract for caching providers
    (InMemoryCache, RedisCache).
    """

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a cached item by key.

        Args:
            key: Cache key string.

        Returns:
            Cached item or None if key is missing/expired.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Stores an item in the cache.

        Args:
            key: Cache key string.
            value: Item value to store.
            ttl_seconds: Optional Time-To-Live in seconds.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Removes an item from the cache.

        Args:
            key: Cache key string.
        """
        pass
