"""
Unit and integration tests for Phase 4 infrastructure adapters, composite geocoding chain,
two-level caching, and system endpoints.
"""

import unittest
from domain.models.location import ResolvedLocation
from infrastructure.geocoding.base_geocoder import BaseGeocoder
from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
from infrastructure.geocoding.composite_geocoder import CompositeGeocoder
from infrastructure.cache.memory_cache import MemoryCache
from infrastructure.cache.redis_cache import RedisCache
from infrastructure.cache.two_level_cache import TwoLevelCache
from infrastructure.cache.cache_factory import create_cache_provider
from infrastructure.container import container, bootstrap_container
from routers.health import health, version, metrics


class FailingGeocoder(BaseGeocoder):
    def geocode(self, place_name: str) -> ResolvedLocation:
        raise ValueError("Provider offline")


class WorkingGeocoder(BaseGeocoder):
    def geocode(self, place_name: str) -> ResolvedLocation:
        return ResolvedLocation(
            resolved_name=place_name,
            latitude=12.34,
            longitude=56.78,
            provider="WorkingGeocoder",
        )


class TestPhase4InfrastructureAndRouters(unittest.TestCase):

    def setUp(self):
        bootstrap_container()

    def test_offline_geocoder_known_city(self):
        geo = OfflineGeocoder()
        loc = geo.geocode("Chennai")
        self.assertEqual(loc.latitude, 13.0827)
        self.assertEqual(loc.longitude, 80.2707)
        self.assertEqual(loc.provider, "OfflineGeocoder")

    def test_composite_geocoder_fallback_chain(self):
        failing1 = FailingGeocoder()
        failing2 = FailingGeocoder()
        working = WorkingGeocoder()

        composite = CompositeGeocoder(providers=[failing1, failing2, working])
        resolved = composite.geocode("TestPlace")

        self.assertEqual(resolved.resolved_name, "TestPlace")
        self.assertEqual(resolved.latitude, 12.34)
        self.assertEqual(resolved.provider, "WorkingGeocoder")

    def test_composite_geocoder_all_failing_raises(self):
        failing1 = FailingGeocoder()
        failing2 = FailingGeocoder()

        composite = CompositeGeocoder(providers=[failing1, failing2])
        with self.assertRaises(ValueError):
            composite.geocode("UnknownPlace")

    def test_memory_cache_l1_stats_and_ttl(self):
        cache = MemoryCache(default_ttl_seconds=10)
        cache.set("key1", "val1")

        self.assertEqual(cache.get("key1"), "val1")
        stats = cache.stats
        self.assertEqual(stats["hits"], 1)
        self.assertEqual(stats["misses"], 0)

        cache.delete("key1")
        self.assertIsNone(cache.get("key1"))

    def test_redis_cache_offline_fallback(self):
        # Pointing to inactive port to test graceful offline fallback
        r = RedisCache(host="127.0.0.1", port=9999)
        self.assertFalse(r.is_connected)
        self.assertIsNone(r.get("any_key"))

    def test_two_level_cache_read_write(self):
        l1 = MemoryCache()
        l2 = RedisCache(host="127.0.0.1", port=9999)  # offline
        two_level = TwoLevelCache(l1_cache=l1, l2_cache=l2)

        two_level.set("k1", "v1")
        self.assertEqual(two_level.get("k1"), "v1")

    def test_cache_factory(self):
        cache = create_cache_provider("two_level")
        self.assertIsInstance(cache, TwoLevelCache)

    def test_health_endpoint(self):
        res = health()
        self.assertEqual(res, {"status": "healthy"})

    def test_version_endpoint(self):
        res = version()
        self.assertEqual(res["status"], "success")
        self.assertIn("metadata", res)
        self.assertEqual(res["metadata"]["api_version"], "1.0.0")

    def test_metrics_endpoint(self):
        res = metrics()
        self.assertEqual(res["status"], "success")
        self.assertIn("cache_stats", res)


if __name__ == "__main__":
    unittest.main()
