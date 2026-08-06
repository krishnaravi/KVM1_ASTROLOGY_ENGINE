"""
L1 In-Memory Cache implementation of ICacheProvider.
"""

import time
from typing import Any, Optional, Dict, Tuple
from core.interfaces.cache_interface import ICacheProvider


class MemoryCache(ICacheProvider):
    """
    L1 In-Memory Cache provider with TTL expiration support.
    """

    def __init__(self, default_ttl_seconds: int = 3600) -> None:
        self.default_ttl_seconds: int = default_ttl_seconds
        # Storage format: key -> (value, expire_timestamp)
        self._store: Dict[str, Tuple[Any, Optional[float]]] = {}
        self._hits: int = 0
        self._misses: int = 0

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            self._misses += 1
            return None

        val, expire_at = self._store[key]
        if expire_at is not None and time.time() > expire_at:
            # Expired item
            del self._store[key]
            self._misses += 1
            return None

        self._hits += 1
        return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        expire_at = (time.time() + ttl) if ttl > 0 else None
        self._store[key] = (value, expire_at)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()
        self._hits = 0
        self._misses = 0

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "entries_count": len(self._store),
            "hits": self._hits,
            "misses": self._misses,
            "hit_ratio": (self._hits / (self._hits + self._misses)) if (self._hits + self._misses) > 0 else 0.0,
        }
