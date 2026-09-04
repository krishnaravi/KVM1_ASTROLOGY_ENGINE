"""
Health, Version, and System Metrics API Routers.
"""

from fastapi import APIRouter
from domain.versioning import ENGINE_METADATA
from infrastructure.container import container
from core.interfaces.cache_interface import ICacheProvider
from infrastructure.cache.two_level_cache import TwoLevelCache
from models.response_models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy"}


@router.get("/api/version", include_in_schema=False)
def version():
    """Returns engine metadata and system versioning details."""
    return {
        "status": "success",
        "metadata": {
            "api_version": ENGINE_METADATA.api_version,
            "engine_version": ENGINE_METADATA.engine_version,
            "rule_version": ENGINE_METADATA.rule_version,
            "ephemeris_version": ENGINE_METADATA.ephemeris_version,
            "build_version": ENGINE_METADATA.build_version,
            "ayanamsa": ENGINE_METADATA.ayanamsa,
        }
    }


@router.get("/api/metrics", include_in_schema=False)
def metrics():
    """Returns runtime cache statistics and system performance metrics."""
    cache_stats = {}
    if container.is_registered(ICacheProvider):
        cache = container.resolve(ICacheProvider)
        if isinstance(cache, TwoLevelCache):
            cache_stats = cache.stats

    return {
        "status": "success",
        "engine": ENGINE_METADATA.engine_version,
        "cache_stats": cache_stats,
    }