"""
Cache Factory for creating Memory, Redis, or TwoLevel cache providers.
"""

from typing import Optional
from core.interfaces.cache_interface import ICacheProvider
from infrastructure.cache.memory_cache import MemoryCache
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.cache.two_level_cache import TwoLevelCache


def create_cache_provider(
    provider_type: str = "two_level",
    l1_ttl_seconds: int = 3600,
    l2_ttl_seconds: int = 86400,
    redis_host: str = "localhost",
    redis_port: int = 6379,
    redis_password: Optional[str] = None,
) -> ICacheProvider:
    """
    Factory function to create the desired cache provider implementation.
    """
    provider_type_clean = provider_type.lower().strip()

    if provider_type_clean == "memory":
        return MemoryCache(default_ttl_seconds=l1_ttl_seconds)
    elif provider_type_clean == "redis":
        return RedisCache(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            default_ttl_seconds=l2_ttl_seconds,
        )
    elif provider_type_clean == "two_level":
        l1 = MemoryCache(default_ttl_seconds=l1_ttl_seconds)
        l2 = RedisCache(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            default_ttl_seconds=l2_ttl_seconds,
        )
        return TwoLevelCache(l1_cache=l1, l2_cache=l2)
    else:
        return MemoryCache(default_ttl_seconds=l1_ttl_seconds)
