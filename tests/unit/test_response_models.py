import unittest

from fastapi.encoders import jsonable_encoder

from models.response_models import (
    HealthResponse,
    HousesResponse,
    LagnaResponse,
    PlanetPositionsResponse,
    RasiChartResponse,
    RootResponse,
)
from main import root
from routers.chart import rasi_chart
from routers.health import health
from routers.house import houses
from routers.lagna import lagna
from routers.planet import planets_positions


class TestResponseModels(unittest.TestCase):

    def setUp(self):
        self.date = "1990-05-15"
        self.time = "10:30"
        self.latitude = 13.0827
        self.longitude = 80.2707
        self.timezone = 5.5

    def test_root_and_health_models(self):
        self.assertEqual(RootResponse.model_validate(root()).model_dump(), root())
        self.assertEqual(HealthResponse.model_validate(health()).model_dump(), health())

    def test_endpoint_models_preserve_payloads(self):
        planet_payload = planets_positions(self.date, self.time, self.timezone)
        lagna_payload = lagna(
            self.date,
            self.time,
            self.latitude,
            self.longitude,
            self.timezone,
        )
        house_payload = houses(
            self.date,
            self.time,
            self.latitude,
            self.longitude,
            self.timezone,
        )
        chart_payload = rasi_chart(
            self.date,
            self.time,
            self.latitude,
            self.longitude,
            self.timezone,
        )

        self.assertEqual(
            PlanetPositionsResponse.model_validate(planet_payload).model_dump(),
            jsonable_encoder(planet_payload),
        )
        self.assertEqual(
            LagnaResponse.model_validate(lagna_payload).model_dump(),
            jsonable_encoder(lagna_payload),
        )
        self.assertEqual(
            HousesResponse.model_validate(house_payload).model_dump(),
            jsonable_encoder(house_payload),
        )
        self.assertEqual(
            RasiChartResponse.model_validate(chart_payload).model_dump(exclude_none=True),
            jsonable_encoder(chart_payload),
        )

    def test_rasi_chart_keys_and_nested_values_survive(self):
        chart = rasi_chart(
            self.date,
            self.time,
            self.latitude,
            self.longitude,
            self.timezone,
        )
        validated = RasiChartResponse.model_validate(chart).model_dump(exclude_none=True)

        self.assertEqual(
            set(validated),
            {
                "lagna",
                "houses",
                "house_lords",
                "house_lord_positions",
                "house_occupants",
                "conjunctions",
                "graha_drishti",
                "yogas",
                "planet_strengths",
                "planet_scores",
                "planets",
            },
        )
        self.assertEqual(validated["houses"][0]["sign"], "கடகம்")
        self.assertEqual(validated["planets"][0]["name"], "Sun")
        self.assertEqual(validated["yogas"][0]["name"], "Budha Aditya Yoga")
        self.assertEqual(validated["planet_strengths"][0]["strength"], "Exalted")
        self.assertEqual(validated["planet_scores"]["Venus"], 100)
        self.assertEqual(validated["planets"][0]["longitude"], chart["planets"][0].longitude)


if __name__ == "__main__":
    unittest.main()