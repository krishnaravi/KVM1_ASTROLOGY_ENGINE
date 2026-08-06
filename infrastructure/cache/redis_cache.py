"""
L2 Redis Cache implementation of ICacheProvider.
"""

import pickle
import logging
from typing import Any, Optional, Dict
from core.interfaces.cache_interface import ICacheProvider

logger = logging.getLogger("kvm1.redis_cache")

try:
    import redis
except ImportError:
    redis = None


class RedisCache(ICacheProvider):
    """
    L2 Redis Cache provider. Gracefully handles connection failures by logging and returning None.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl_seconds: int = 86400,
    ) -> None:
        self.default_ttl_seconds: int = default_ttl_seconds
        self._client: Optional[Any] = None
        self._is_connected: bool = False

        if redis:
            try:
                self._client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    socket_timeout=1.0,
                )
                # Quick ping check
                self._client.ping()
                self._is_connected = True
            except Exception as e:
                logger.warning(f"Redis cache connection unavailable: {str(e)}")
                self._client = None
                self._is_connected = False

    def get(self, key: str) -> Optional[Any]:
        if not self._is_connected or not self._client:
            return None
        try:
            val = self._client.get(key)
            if val is not None:
                return pickle.loads(val)
        except Exception as e:
            logger.warning(f"Redis GET failed for key '{key}': {str(e)}")
        return None

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        if not self._is_connected or not self._client:
            return
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        try:
            serialized = pickle.dumps(value)
            self._client.set(name=key, value=serialized, ex=ttl)
        except Exception as e:
            logger.warning(f"Redis SET failed for key '{key}': {str(e)}")

    def delete(self, key: str) -> None:
        if not self._is_connected or not self._client:
            return
        try:
            self._client.delete(key)
        except Exception as e:
            logger.warning(f"Redis DELETE failed for key '{key}': {str(e)}")

    @property
    def is_connected(self) -> bool:
        return self._is_connected
