import unittest
from dataclasses import FrozenInstanceError
from domain import (
    BirthData,
    ResolvedLocation,
    TimezoneContext,
    JulianDayContext,
    EphemerisContext,
    AstronomicalState,
    CalculationContext,
    CalculationAuditLog,
    EngineMetadata,
    ENGINE_METADATA,
    API_VERSION,
    ENGINE_VERSION,
    RULE_VERSION,
    EPHEMERIS_VERSION,
)
from validators.birth_data_validator import BirthDataValidator


class TestPhase1DomainAndValidation(unittest.TestCase):

    def test_engine_metadata_instance(self):
        self.assertIsInstance(ENGINE_METADATA, EngineMetadata)
        self.assertEqual(ENGINE_METADATA.api_version, "1.0.0")
        self.assertEqual(ENGINE_METADATA.engine_version, "2.0.0")
        self.assertEqual(ENGINE_METADATA.rule_version, "1.0.0")
        self.assertEqual(ENGINE_METADATA.ephemeris_version, "Swiss Ephemeris 2.10.03")
        self.assertEqual(ENGINE_METADATA.build_version, "2.0.0-build.1")
        self.assertEqual(ENGINE_METADATA.ayanamsa, "Lahiri")

    def test_version_constants_backward_compatibility(self):
        self.assertEqual(API_VERSION, ENGINE_METADATA.api_version)
        self.assertEqual(ENGINE_VERSION, ENGINE_METADATA.engine_version)
        self.assertEqual(RULE_VERSION, ENGINE_METADATA.rule_version)
        self.assertEqual(EPHEMERIS_VERSION, ENGINE_METADATA.ephemeris_version)

    def test_domain_dataclasses_are_frozen(self):
        bd = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        with self.assertRaises(FrozenInstanceError):
            bd.date = "1991-01-01"

        loc = ResolvedLocation(resolved_name="Chennai", latitude=13.0, longitude=80.0)
        with self.assertRaises(FrozenInstanceError):
            loc.latitude = 14.0

        tz = TimezoneContext(iana_timezone="Asia/Kolkata", utc_offset="+05:30", utc_offset_seconds=19800, is_dst=False)
        with self.assertRaises(FrozenInstanceError):
            tz.iana_timezone = "UTC"

        meta = EngineMetadata()
        with self.assertRaises(FrozenInstanceError):
            meta.api_version = "2.0.0"

    def test_birth_data_validator_success_coords(self):
        data = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=80.2707)
        res = BirthDataValidator.validate(data)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)

    def test_birth_data_validator_success_place(self):
        data = BirthData(date="1990-05-15", time="10:30:45", birth_place="Chennai, India")
        res = BirthDataValidator.validate(data)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)

    def test_birth_data_validator_invalid_date(self):
        data = BirthData(date="1990-02-31", time="10:30", latitude=13.0827, longitude=80.2707)
        res = BirthDataValidator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Invalid date format" in e for e in res.errors))

    def test_birth_data_validator_invalid_time(self):
        data = BirthData(date="1990-05-15", time="25:70", latitude=13.0827, longitude=80.2707)
        res = BirthDataValidator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Invalid time format" in e for e in res.errors))

    def test_birth_data_validator_missing_location(self):
        data = BirthData(date="1990-05-15", time="10:30")
        res = BirthDataValidator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Either 'birth_place' or both 'latitude' and 'longitude'" in e for e in res.errors))

    def test_birth_data_validator_lat_out_of_bounds(self):
        data = BirthData(date="1990-05-15", time="10:30", latitude=95.0, longitude=80.2707)
        res = BirthDataValidator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Latitude" in e for e in res.errors))

    def test_birth_data_validator_lon_out_of_bounds(self):
        data = BirthData(date="1990-05-15", time="10:30", latitude=13.0827, longitude=190.0)
        res = BirthDataValidator.validate(data)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Longitude" in e for e in res.errors))

    def test_calculation_context_instantiation(self):
        birth_data = BirthData(date="1990-05-15", time="10:30", birth_place="Chennai, India")
        loc = ResolvedLocation(resolved_name="Chennai, India", latitude=13.0827, longitude=80.2707, provider="Offline")
        tz = TimezoneContext(iana_timezone="Asia/Kolkata", utc_offset="+05:30", utc_offset_seconds=19800, is_dst=False)
        jd = JulianDayContext(local_datetime="1990-05-15T10:30:00+05:30", utc_datetime="1990-05-15T05:00:00Z", julian_day=2448026.70833)
        eph = EphemerisContext(ephemeris_version=EPHEMERIS_VERSION, ayanamsa_name="Lahiri", ayanamsa_value=23.73)
        astro = AstronomicalState(julian_day=2448026.70833, ayanamsa_deg=23.73)

        ctx = CalculationContext(
            trace_id="test-trace-123",
            birth_data=birth_data,
            resolved_location=loc,
            timezone_context=tz,
            julian_day_context=jd,
            ephemeris_context=eph,
            astronomical_state=astro,
        )

        self.assertEqual(ctx.trace_id, "test-trace-123")
        self.assertEqual(ctx.birth_data.date, "1990-05-15")
        self.assertEqual(ctx.resolved_location.latitude, 13.0827)
        self.assertEqual(ctx.timezone_context.iana_timezone, "Asia/Kolkata")
        self.assertEqual(ctx.julian_day_context.julian_day, 2448026.70833)
        self.assertEqual(ctx.ephemeris_context.ayanamsa_name, "Lahiri")
        self.assertEqual(ctx.astronomical_state.ayanamsa_deg, 23.73)


if __name__ == "__main__":
    unittest.main()
