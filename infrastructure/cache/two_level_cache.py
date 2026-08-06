"""
Two-Level Cache implementation of ICacheProvider.
Combines L1 Memory Cache and L2 Redis Cache.
"""

from typing import Any, Optional, Dict
from core.interfaces.cache_interface import ICacheProvider
from infrastructure.cache.memory_cache import MemoryCache
from infrastructure.cache.redis_cache import RedisCache


class TwoLevelCache(ICacheProvider):
    """
    Two-Level Cache Provider (L1 Memory Cache + L2 Redis Cache).

    Read Flow:
        1. Check L1 Memory Cache. If HIT -> Return value immediately.
        2. If L1 MISS -> Check L2 Redis Cache.
        3. If L2 HIT -> Populate L1 Memory Cache and Return value.
        4. If both MISS -> Return None.

    Write Flow:
        Write value to both L1 Memory Cache and L2 Redis Cache.
    """

    def __init__(
        self,
        l1_cache: Optional[MemoryCache] = None,
        l2_cache: Optional[RedisCache] = None,
    ) -> None:
        self.l1: MemoryCache = l1_cache or MemoryCache(default_ttl_seconds=3600)
        self.l2: RedisCache = l2_cache or RedisCache(default_ttl_seconds=86400)

    def get(self, key: str) -> Optional[Any]:
        # 1. L1 Memory Check
        val = self.l1.get(key)
        if val is not None:
            return val

        # 2. L2 Redis Check
        val = self.l2.get(key)
        if val is not None:
            # Populate L1 on L2 hit
            self.l1.set(key, val, ttl_seconds=3600)
            return val

        return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        self.l1.set(key, value, ttl_seconds=ttl_seconds)
        self.l2.set(key, value, ttl_seconds=ttl_seconds)

    def delete(self, key: str) -> None:
        self.l1.delete(key)
        self.l2.delete(key)

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "l1_memory": self.l1.stats,
            "l2_redis_connected": self.l2.is_connected,
        }
