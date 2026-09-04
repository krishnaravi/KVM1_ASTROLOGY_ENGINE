import unittest

from fastapi import HTTPException

from main import app, calculate_horoscope
from routers.chart import rasi_chart
from routers.house import houses
from routers.lagna import lagna
from routers.planet import planets_positions
from validators.api_input_validator import validate_api_inputs


class TestApiInputValidation(unittest.TestCase):

    def assert_unprocessable(self, call):
        with self.assertRaises(HTTPException) as context:
            call()
        self.assertEqual(context.exception.status_code, 422)

    def test_invalid_calendar_date(self):
        self.assert_unprocessable(lambda: planets_positions("2023-02-30", "12:00"))

    def test_invalid_time(self):
        self.assert_unprocessable(lambda: planets_positions("2023-02-28", "25:00"))

    def test_valid_time_formats(self):
        self.assertEqual(planets_positions("2023-02-28", "12:00")["status"], "success")
        self.assertEqual(planets_positions("2023-02-28", "12:00:30")["status"], "success")

    def test_latitude_boundaries_and_range(self):
        validate_api_inputs("2023-02-28", "12:00", -90, 0, require_location=True)
        validate_api_inputs("2023-02-28", "12:00", 90, 0, require_location=True)
        self.assert_unprocessable(lambda: lagna("2023-02-28", "12:00", -90.1, 0))
        self.assert_unprocessable(lambda: lagna("2023-02-28", "12:00", 90.1, 0))

    def test_longitude_boundaries_and_range(self):
        validate_api_inputs("2023-02-28", "12:00", 0, -180, require_location=True)
        validate_api_inputs("2023-02-28", "12:00", 0, 180, require_location=True)
        self.assert_unprocessable(lambda: houses("2023-02-28", "12:00", 0, -180.1))
        self.assert_unprocessable(lambda: houses("2023-02-28", "12:00", 0, 180.1))

    def test_timezone_boundaries_and_range(self):
        for timezone in (-12, 14):
            self.assertEqual(
                planets_positions("2023-02-28", "12:00", timezone)["status"],
                "success",
            )
        self.assert_unprocessable(lambda: planets_positions("2023-02-28", "12:00", -12.1))
        self.assert_unprocessable(lambda: planets_positions("2023-02-28", "12:00", 14.1))

    def test_missing_required_parameters_are_documented(self):
        paths = app.openapi()["paths"]
        for path in ("/api/lagna", "/api/houses", "/api/rasi-chart"):
            required = {
                parameter["name"]
                for parameter in paths[path]["get"]["parameters"]
                if parameter.get("required")
            }
            self.assertTrue({"date", "time", "latitude", "longitude"}.issubset(required))

    def test_legacy_invalid_input_returns_http_422(self):
        self.assert_unprocessable(lambda: calculate_horoscope("2023-02-30", "12:00"))

    def test_all_calculation_routes_validate_inputs(self):
        invalid = ("2023-02-30", "25:00", 0, 0, 0)
        for call in (
            lambda: lagna(*invalid),
            lambda: houses(*invalid),
            lambda: rasi_chart(*invalid),
        ):
            self.assert_unprocessable(call)


if __name__ == "__main__":
    unittest.main()