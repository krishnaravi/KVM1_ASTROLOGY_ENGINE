import unittest

from core.swisseph_service import get_julian_day, get_utc_datetime


class TestTimezoneJulianDay(unittest.TestCase):

    def test_utc_timezone(self):
        utc_dt = get_utc_datetime("1990-05-15", "05:30", 0)

        self.assertEqual(utc_dt.isoformat(), "1990-05-15T05:30:00+00:00")
        self.assertAlmostEqual(
            get_julian_day("1990-05-15", "05:30", 0),
            2448026.7291666665,
            places=6,
        )

    def test_ist_fractional_offset(self):
        utc_dt = get_utc_datetime("1990-05-15", "11:00", 5.5)

        self.assertEqual(utc_dt.isoformat(), "1990-05-15T05:30:00+00:00")
        self.assertAlmostEqual(
            get_julian_day("1990-05-15", "11:00", 5.5),
            2448026.7291666665,
            places=6,
        )

    def test_positive_offset_rolls_back_to_previous_utc_date(self):
        utc_dt = get_utc_datetime("2024-01-02", "00:30", 5.5)

        self.assertEqual(utc_dt.isoformat(), "2024-01-01T19:00:00+00:00")
        self.assertAlmostEqual(
            get_julian_day("2024-01-02", "00:30", 5.5),
            2460311.2916666665,
            places=6,
        )

    def test_negative_offset_rolls_forward_to_next_utc_date(self):
        utc_dt = get_utc_datetime("2024-01-01", "23:30", -5.5)

        self.assertEqual(utc_dt.isoformat(), "2024-01-02T05:00:00+00:00")
        self.assertAlmostEqual(
            get_julian_day("2024-01-01", "23:30", -5.5),
            2460311.7083333335,
            places=6,
        )


if __name__ == "__main__":
    unittest.main()