"""
Unit and regression tests for Phase 6 Divisional Charts (Varga) Engine and VargaRegistry.
"""

import unittest
from domain.models.birth_data import BirthData
from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
from services.location_service import LocationService
from services.timezone_service import TimezoneService
from services.julian_day_service import JulianDayService
from services.swisseph_service import SwissephService
from services.calculation_pipeline import CalculationPipeline
from vargas.registry import VargaRegistry, bootstrap_vargas, varga_registry
from vargas.calculators import (
    D2HoraCalculator,
    D3DrekkanaCalculator,
    D7SaptamsaCalculator,
    D9NavamsaCalculator,
    D10DasamsaCalculator,
    D12DwadasamsaCalculator,
    D16ShodasamsaCalculator,
    D20VimsamsaCalculator,
    D24ChaturvimsamsaCalculator,
    D27BhamsaCalculator,
    D30TrimsamsaCalculator,
    D40KhavedamsaCalculator,
    D45AkshavedamsaCalculator,
    D60ShastiamsaCalculator,
)


class TestPhase6VargaEngine(unittest.TestCase):

    def setUp(self):
        self.registry = VargaRegistry()
        bootstrap_vargas(self.registry)

        self.pipeline = CalculationPipeline(
            stages=[
                LocationService(geocoder=OfflineGeocoder()),
                TimezoneService(),
                JulianDayService(),
                SwissephService(),
            ]
        )
        bd = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai")
        self.context = self.pipeline.execute(bd, trace_id="varga-test-trace")

    def test_varga_registry_all_14_registered(self):
        expected_vargas = ["D2", "D3", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]
        for code in expected_vargas:
            self.assertTrue(self.registry.is_registered(code), f"Varga '{code}' should be registered")
            calc = self.registry.get(code)
            self.assertEqual(calc.varga_code, code)

    def test_varga_registry_unregistered_raises(self):
        with self.assertRaises(KeyError):
            self.registry.get("D99")

    def test_d9_navamsa_math(self):
        d9 = D9NavamsaCalculator()
        # 15° Taurus (Taurus=1 [Earthy], starts Capricorn=9). 15° / 3.333° = part 4. Cap(9)+4 = Taurus(1)
        sign, deg = d9.calculate_varga_sign(45.0)  # 45° = 15° Taurus
        self.assertEqual(sign, "ரிஷபம்")  # Taurus
        self.assertAlmostEqual(deg, 15.0, places=4)

    def test_d10_dasamsa_math(self):
        d10 = D10DasamsaCalculator()
        # 5° Aries (Aries=0 [Odd], starts Aries). 5° / 3.0 = part 1. Aries(0)+1 = Taurus(1)
        sign, deg = d10.calculate_varga_sign(5.0)
        self.assertEqual(sign, "ரிஷபம்")  # Taurus
        self.assertAlmostEqual(deg, 20.0, places=4)

    def test_varga_chart_generation(self):
        for code in ["D2", "D3", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]:
            calc = self.registry.get(code)
            chart = calc.calculate_varga_chart(self.context)

            self.assertEqual(chart["varga_code"], code)
            self.assertIn("varga_ascendant", chart)
            self.assertIn("planets", chart)
            self.assertEqual(len(chart["planets"]), 9)


if __name__ == "__main__":
    unittest.main()
