import unittest
from typing import Optional, Any, Dict, List, Tuple
from core.interfaces import (
    IGeocoderProvider,
    ICacheProvider,
    ITimezoneService,
    IJulianDayService,
    ISwissephService,
    IAstrologyEngine,
    IRule,
    RuleResult,
    IRuleEngine,
    IAuditLogger,
)
from domain import (
    ResolvedLocation,
    TimezoneContext,
    JulianDayContext,
    CalculationContext,
    CalculationAuditLog,
)
from infrastructure.container import Container, DependencyResolutionError


class DummyGeocoder(IGeocoderProvider):
    def geocode(self, place_name: str) -> ResolvedLocation:
        return ResolvedLocation(resolved_name=place_name, latitude=10.0, longitude=20.0, provider="Dummy")


class DummyCache(ICacheProvider):
    def __init__(self):
        self.store = {}

    def get(self, key: str) -> Optional[Any]:
        return self.store.get(key)

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        self.store[key] = value

    def delete(self, key: str) -> None:
        self.store.pop(key, None)


class DummyEngine(IAstrologyEngine):
    @property
    def engine_id(self) -> str:
        return "dummy"

    @property
    def version(self) -> str:
        return "1.0.0"

    def calculate(self, context: CalculationContext) -> Dict[str, Any]:
        return {"status": "calculated", "trace_id": context.trace_id}


class TestPhase2InterfacesAndContainer(unittest.TestCase):

    def test_interfaces_cannot_be_instantiated_directly(self):
        interfaces = [
            IGeocoderProvider,
            ICacheProvider,
            ITimezoneService,
            IJulianDayService,
            ISwissephService,
            IAstrologyEngine,
            IRule,
            IRuleEngine,
            IAuditLogger,
        ]
        for interface in interfaces:
            with self.assertRaises(TypeError):
                interface()

    def test_concrete_geocoder_implementation(self):
        geocoder = DummyGeocoder()
        loc = geocoder.geocode("TestCity")
        self.assertEqual(loc.resolved_name, "TestCity")
        self.assertEqual(loc.latitude, 10.0)
        self.assertEqual(loc.longitude, 20.0)
        self.assertEqual(loc.provider, "Dummy")

    def test_concrete_cache_implementation(self):
        cache = DummyCache()
        cache.set("key1", "val1")
        self.assertEqual(cache.get("key1"), "val1")
        cache.delete("key1")
        self.assertIsNone(cache.get("key1"))

    def test_container_singleton_registration(self):
        c = Container()
        cache_instance = DummyCache()
        c.register_singleton(ICacheProvider, cache_instance)

        self.assertTrue(c.is_registered(ICacheProvider))
        resolved = c.resolve(ICacheProvider)
        self.assertIs(resolved, cache_instance)

    def test_container_factory_registration(self):
        c = Container()
        c.register_factory(IGeocoderProvider, lambda container: DummyGeocoder())

        self.assertTrue(c.is_registered(IGeocoderProvider))
        inst1 = c.resolve(IGeocoderProvider)
        inst2 = c.resolve(IGeocoderProvider)
        self.assertIsNot(inst1, inst2)
        self.assertIsInstance(inst1, DummyGeocoder)

    def test_container_instance_override(self):
        c = Container()
        mock_engine = DummyEngine()
        c.register_instance(IAstrologyEngine, mock_engine)

        resolved = c.resolve(IAstrologyEngine)
        self.assertIs(resolved, mock_engine)

    def test_container_unregistered_resolution_raises(self):
        c = Container()
        with self.assertRaises(DependencyResolutionError):
            c.resolve(ITimezoneService)

    def test_container_clear(self):
        c = Container()
        c.register_singleton(ICacheProvider, DummyCache())
        self.assertTrue(c.is_registered(ICacheProvider))
        c.clear()
        self.assertFalse(c.is_registered(ICacheProvider))


if __name__ == "__main__":
    unittest.main()
