"""
Unit and regression tests for Phase 7 Rule Engine Framework.
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
from rules.registry import RuleRegistry, bootstrap_rules, rule_registry
from rules.rule_engine import RuleEngine


class TestPhase7RuleEngine(unittest.TestCase):

    def setUp(self):
        self.rule_reg = RuleRegistry()
        bootstrap_rules(self.rule_reg)
        self.rule_engine = RuleEngine(registry=self.rule_reg)

        # Build pipeline context and run VedicEngine
        pipeline = CalculationPipeline(
            stages=[
                LocationService(geocoder=OfflineGeocoder()),
                TimezoneService(),
                JulianDayService(),
                SwissephService(),
            ]
        )
        bd = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai")
        self.context = pipeline.execute(bd, trace_id="rule-test-trace")

        eng_reg = EngineRegistry()
        bootstrap_engines(eng_reg)
        vedic_engine = eng_reg.get("vedic")
        self.engine_outputs = vedic_engine.calculate(self.context)

    def test_rule_registry_categories_and_priorities(self):
        categories = ["classical", "yoga", "raja_yoga", "dhana_yoga", "arishta", "neecha_bhanga", "functional_dignity"]
        for cat in categories:
            rules = self.rule_reg.get_by_category(cat)
            self.assertTrue(len(rules) > 0, f"Category '{cat}' should have registered rules")

        # Verify priority sorting descending
        all_rules = self.rule_reg.list_all_rules()
        priorities = [r.priority for r in all_rules]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_rule_engine_evaluate_all_priority_order(self):
        results = self.rule_engine.evaluate_all(
            context=self.context,
            engine_outputs=self.engine_outputs,
        )
        self.assertEqual(len(results), 7)
        priorities = [res.priority for res in results]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_rule_engine_evaluate_category(self):
        yoga_results = self.rule_engine.evaluate_category(
            category="yoga",
            context=self.context,
            engine_outputs=self.engine_outputs,
        )
        self.assertEqual(len(yoga_results), 1)
        self.assertEqual(yoga_results[0].category, "yoga")

    def test_all_7_rule_categories_return_valid_rule_results(self):
        results = self.rule_engine.evaluate_all(
            context=self.context,
            engine_outputs=self.engine_outputs,
        )
        for res in results:
            self.assertIsNotNone(res.rule_id)
            self.assertIsNotNone(res.category)
            self.assertIsInstance(res.triggered, bool)
            self.assertTrue(0.0 <= res.confidence_score <= 1.0)
            self.assertIsInstance(res.payload, dict)


if __name__ == "__main__":
    unittest.main()
