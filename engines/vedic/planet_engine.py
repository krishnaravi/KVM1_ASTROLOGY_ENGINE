"""
Vedic Planet Engine.
Maps raw astronomical planets from AstronomicalState to horoscope house placements.
"""

from typing import List
from domain.models.calculation_context import CalculationContext
from domain.planet import Planet
from domain.chart import ChartPlanet
from domain.house import House


class VedicPlanetEngine:
    """
    Sub-engine responsible for placed ChartPlanet calculation.
    Pure functional engine reading exclusively from AstronomicalState.
    """

    @staticmethod
    def _get_planet_house(planet_longitude: float, houses: List[House]) -> int:
        """Determines house number (1-12) for a given planet longitude."""
        if not houses:
            return int(planet_longitude // 30) + 1

        sorted_houses = sorted(houses, key=lambda h: h.number)
        num_houses = len(sorted_houses)

        for i, h in enumerate(sorted_houses):
            start = h.longitude
            if i == num_houses - 1:
                end = sorted_houses[0].longitude + 360.0
            else:
                end = sorted_houses[i + 1].longitude

            lon = planet_longitude
            if lon < start:
                lon += 360.0

            if start <= lon < end:
                return h.number

        return 1

    def calculate_chart_planets(self, context: CalculationContext) -> List[ChartPlanet]:
        """
        Maps raw astronomical planets to ChartPlanet entities with house placements.
        """
        if not context.astronomical_state:
            raise ValueError("AstronomicalState is required for VedicPlanetEngine calculation.")

        raw_planets: List[Planet] = context.astronomical_state.planets
        houses: List[House] = context.astronomical_state.houses

        chart_planets: List[ChartPlanet] = []
        for p in raw_planets:
            house_num = self._get_planet_house(p.longitude, houses)
            chart_planets.append(
                ChartPlanet(
                    name=p.name,
                    longitude=p.longitude,
                    latitude=p.latitude,
                    speed=p.speed,
                    retrograde=p.retrograde,
                    sign=p.sign,
                    degree_in_sign=p.degree_in_sign,
                    house=house_num,
                    nakshatra=p.nakshatra,
                    nakshatra_lord=p.nakshatra_lord,
                    pada=p.pada,
                )
            )

        return chart_planets
