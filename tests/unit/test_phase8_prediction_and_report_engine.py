"""
Unit and integration tests for Phase 8 Prediction Engine, Explanation Engine, Report Builder, and JSON Response Builder.
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
from rules.registry import RuleRegistry, bootstrap_rules
from rules.rule_engine import RuleEngine
from predictions.explanation_engine import ExplanationEngine
from predictions.prediction_engine import PredictionEngine
from reports.report_builder import ReportBuilder
from reports.json_response_builder import JSONResponseBuilder


class TestPhase8PredictionAndReportEngine(unittest.TestCase):

    def setUp(self):
        # 1. Pipeline Execution
        pipeline = CalculationPipeline(
            stages=[
                LocationService(geocoder=OfflineGeocoder()),
                TimezoneService(),
                JulianDayService(),
                SwissephService(),
            ]
        )
        bd = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai")
        self.context = pipeline.execute(bd, trace_id="prediction-test-trace")

        # 2. Vedic Engine Execution
        eng_reg = EngineRegistry()
        bootstrap_engines(eng_reg)
        vedic_engine = eng_reg.get("vedic")
        self.vedic_output = vedic_engine.calculate(self.context)

        # 3. Rule Engine Execution
        rule_reg = RuleRegistry()
        bootstrap_rules(rule_reg)
        rule_engine = RuleEngine(registry=rule_reg)
        self.rule_results = rule_engine.evaluate_all(
            context=self.context,
            engine_outputs=self.vedic_output,
        )

        self.explanation_engine = ExplanationEngine()
        self.prediction_engine = PredictionEngine(explanation_engine=self.explanation_engine)
        self.report_builder = ReportBuilder()
        self.response_builder = JSONResponseBuilder()

    def test_explanation_engine_multilingual(self):
        exp_ta = self.explanation_engine.explain_rule("RULE_YOGA_BUDHA_ADITYA", lang="ta")
        exp_en = self.explanation_engine.explain_rule("RULE_YOGA_BUDHA_ADITYA", lang="en")

        self.assertIn("புத-ஆதித்ய யோகத்தை", exp_ta)
        self.assertIn("Budha-Aditya Yoga", exp_en)

    def test_prediction_engine_output_structure(self):
        pred_ta = self.prediction_engine.generate_prediction(
            context=self.context,
            rule_results=self.rule_results,
            vedic_output=self.vedic_output,
            lang="ta",
        )

        self.assertIn("summary", pred_ta)
        self.assertIn("strengths", pred_ta)
        self.assertIn("weaknesses", pred_ta)
        self.assertIn("yogas", pred_ta)
        self.assertIn("doshas", pred_ta)
        self.assertIn("recommendations", pred_ta)
        self.assertIn("confidence_score", pred_ta)
        self.assertEqual(pred_ta["trace_id"], "prediction-test-trace")

    def test_report_builder_and_json_response_builder(self):
        pred = self.prediction_engine.generate_prediction(
            context=self.context,
            rule_results=self.rule_results,
            vedic_output=self.vedic_output,
            lang="en",
        )
        report = self.report_builder.build_report_sections(pred)
        response = self.response_builder.build_response(pred, report)

        self.assertEqual(response["status"], "success")
        self.assertIn("summary", response)
        self.assertIn("confidence_score", response)
        self.assertEqual(response["trace_id"], "prediction-test-trace")
        self.assertIn("report", response)
        self.assertIn("sections", response["report"])


if __name__ == "__main__":
    unittest.main()
