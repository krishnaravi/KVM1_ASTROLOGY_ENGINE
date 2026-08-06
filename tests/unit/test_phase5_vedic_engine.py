"""
Unit and regression tests for Phase 5 Vedic Core Calculation Engine and EngineRegistry.
"""

import unittest
from domain.models.birth_data import BirthData
from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
from services.location_service import LocationService
from services.timezone_service import TimezoneService
from services.julian_day_service import JulianDayService
from services.swisseph_service import SwissephService
from services.calculation_pipeline import CalculationPipeline
from engines.registry import EngineRegistry, bootstrap_engines
from engines.vedic.vedic_engine import VedicEngine
from engines.vedic.planet_engine import VedicPlanetEngine
from engines.vedic.house_engine import VedicHouseEngine
from engines.vedic.house_lord_engine import VedicHouseLordEngine
from engines.vedic.drishti_engine import VedicDrishtiEngine
from engines.vedic.strength_engine import VedicStrengthEngine


class TestPhase5VedicEngine(unittest.TestCase):

    def setUp(self):
        self.registry = EngineRegistry()
        bootstrap_engines(self.registry)

        # Build pipeline context
        self.pipeline = CalculationPipeline(
            stages=[
                LocationService(geocoder=OfflineGeocoder()),
                TimezoneService(),
                JulianDayService(),
                SwissephService(),
            ]
        )
        bd = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai")
        self.context = self.pipeline.execute(bd, trace_id="vedic-test-trace")

    def test_engine_registry_bootstrap(self):
        self.assertTrue(self.registry.is_registered("vedic"))
        engine = self.registry.get("vedic")
        self.assertIsInstance(engine, VedicEngine)
        self.assertEqual(engine.engine_id, "vedic")
        self.assertEqual(engine.version, "2.0.0")

    def test_engine_registry_unregistered_raises(self):
        with self.assertRaises(KeyError):
            self.registry.get("nonexistent_engine")

    def test_vedic_planet_engine(self):
        pe = VedicPlanetEngine()
        planets = pe.calculate_chart_planets(self.context)
        self.assertEqual(len(planets), 9)
        for p in planets:
            self.assertTrue(1 <= p.house <= 12)

    def test_vedic_house_engine(self):
        pe = VedicPlanetEngine()
        planets = pe.calculate_chart_planets(self.context)
        he = VedicHouseEngine()
        res = he.calculate_houses_and_occupants(self.context, planets)

        self.assertIn("houses", res)
        self.assertEqual(len(res["houses"]), 12)
        self.assertIn("house_occupants", res)

    def test_vedic_house_lord_engine(self):
        pe = VedicPlanetEngine()
        planets = pe.calculate_chart_planets(self.context)
        hle = VedicHouseLordEngine()
        res = hle.calculate_house_lords(self.context.astronomical_state.houses, planets)

        self.assertIn("house_lords", res)
        self.assertIn("house_lord_positions", res)
        self.assertEqual(len(res["house_lords"]), 12)

    def test_vedic_drishti_engine(self):
        pe = VedicPlanetEngine()
        planets = pe.calculate_chart_planets(self.context)
        de = VedicDrishtiEngine()
        drishti = de.calculate_graha_drishti(planets)

        self.assertIn("Sun", drishti)
        self.assertIn("Mars", drishti)
        # Mars should aspect 3 houses (4th, 7th, 8th from placement)
        self.assertEqual(len(drishti["Mars"]), 3)

    def test_vedic_strength_engine(self):
        pe = VedicPlanetEngine()
        planets = pe.calculate_chart_planets(self.context)
        se = VedicStrengthEngine()
        res = se.calculate_strengths_and_scores(planets)

        self.assertIn("strengths", res)
        self.assertIn("scores", res)
        self.assertIn("Sun", res["scores"])

    def test_vedic_engine_end_to_end(self):
        vedic_engine = self.registry.get("vedic")
        out = vedic_engine.calculate(self.context)

        self.assertEqual(out["engine_id"], "vedic")
        self.assertEqual(out["version"], "2.0.0")
        self.assertEqual(len(out["planets"]), 9)
        self.assertEqual(len(out["houses"]), 12)
        self.assertIn("house_lords", out)
        self.assertIn("graha_drishti", out)
        self.assertIn("planet_strengths", out)
        self.assertIn("planet_scores", out)


if __name__ == "__main__":
    unittest.main()
