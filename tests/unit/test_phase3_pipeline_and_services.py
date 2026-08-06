"""
Unit tests for Phase 3 services, error handling, stage metrics, and pipeline orchestration.
"""

import unittest
from domain.models.birth_data import BirthData
from domain.models.calculation_context import CalculationContext
from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
from infrastructure.container import Container, bootstrap_container
from services.location_service import LocationService
from services.timezone_service import TimezoneService
from services.julian_day_service import JulianDayService
from services.swisseph_service import SwissephService
from services.audit_logging_service import AuditLoggingService
from services.calculation_pipeline import CalculationPipeline
from core.errors import ValidationError, LocationResolutionError


class TestPhase3PipelineAndServices(unittest.TestCase):

    def setUp(self):
        self.container = Container()
        bootstrap_container(self.container)

        self.geocoder = OfflineGeocoder()
        self.loc_service = LocationService(geocoder=self.geocoder)
        self.tz_service = TimezoneService()
        self.jd_service = JulianDayService()
        self.swe_service = SwissephService()
        self.audit_logger = AuditLoggingService()

        self.pipeline = CalculationPipeline(
            stages=[
                self.loc_service,
                self.tz_service,
                self.jd_service,
                self.swe_service,
            ],
            audit_logger=self.audit_logger,
        )

    def test_location_service_direct_coords(self):
        bd = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        ctx = CalculationContext(trace_id="t-1", birth_data=bd)
        enriched = self.loc_service.process(ctx)

        self.assertIsNotNone(enriched.resolved_location)
        self.assertEqual(enriched.resolved_location.latitude, 13.0827)
        self.assertEqual(enriched.resolved_location.longitude, 80.2707)
        self.assertEqual(enriched.context_version, 1)
        self.assertEqual(len(enriched.stage_metrics), 1)

    def test_timezone_service_chennai(self):
        bd = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        ctx = CalculationContext(trace_id="t-2", birth_data=bd)
        ctx = self.loc_service.process(ctx)
        ctx = self.tz_service.process(ctx)

        self.assertIsNotNone(ctx.timezone_context)
        self.assertEqual(ctx.timezone_context.iana_timezone, "Asia/Kolkata")
        self.assertEqual(ctx.timezone_context.utc_offset, "+05:30")
        self.assertFalse(ctx.timezone_context.is_dst)

    def test_julian_day_service(self):
        bd = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        ctx = CalculationContext(trace_id="t-3", birth_data=bd)
        ctx = self.loc_service.process(ctx)
        ctx = self.tz_service.process(ctx)
        ctx = self.jd_service.process(ctx)

        self.assertIsNotNone(ctx.julian_day_context)
        self.assertTrue(ctx.julian_day_context.utc_datetime.endswith("05:00:00+00:00") or "05:00:00" in ctx.julian_day_context.utc_datetime)
        self.assertAlmostEqual(ctx.julian_day_context.julian_day, 2448026.7083333335, places=4)

    def test_swisseph_service(self):
        bd = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        ctx = CalculationContext(trace_id="t-4", birth_data=bd)
        ctx = self.loc_service.process(ctx)
        ctx = self.tz_service.process(ctx)
        ctx = self.jd_service.process(ctx)
        ctx = self.swe_service.process(ctx)

        self.assertIsNotNone(ctx.ephemeris_context)
        self.assertEqual(ctx.ephemeris_context.ayanamsa_name, "Lahiri")
        self.assertIsNotNone(ctx.astronomical_state)
        self.assertEqual(len(ctx.astronomical_state.planets), 9)  # 7 grahas + Rahu + Ketu
        self.assertEqual(len(ctx.astronomical_state.houses), 12)

    def test_pipeline_end_to_end_place_input(self):
        bd = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai, India")
        ctx = self.pipeline.execute(bd, trace_id="trace-e2e-1")

        self.assertEqual(ctx.trace_id, "trace-e2e-1")
        self.assertEqual(ctx.resolved_location.resolved_name, "Chennai, Tamil Nadu, India")
        self.assertEqual(ctx.timezone_context.iana_timezone, "Asia/Kolkata")
        self.assertEqual(len(ctx.stage_metrics), 4)

        # Verify Stage metrics taxonomy & versions
        for idx, metric in enumerate(ctx.stage_metrics):
            self.assertEqual(metric.status, "SUCCESS")
            self.assertEqual(metric.input_context_version, idx)
            self.assertEqual(metric.output_context_version, idx + 1)
            self.assertGreaterEqual(metric.execution_time_ms, 0.0)

        # Verify Audit Log entry recorded
        logs = self.audit_logger.get_logged_records()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].trace_id, "trace-e2e-1")

    def test_pipeline_validation_error(self):
        bd = BirthData(date="invalid-date", time="10:30", birth_place="Chennai")
        with self.assertRaises(ValidationError) as cm:
            self.pipeline.execute(bd)
        self.assertIn("VALIDATION_ERROR", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
