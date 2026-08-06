"""
Vedic Calculation Engine implementing IAstrologyEngine.
Composite calculation engine reading exclusively from AstronomicalState.
"""

from typing import Dict, Any, List
from core.interfaces.engine_interface import IAstrologyEngine
from domain.models.calculation_context import CalculationContext
from engines.vedic.planet_engine import VedicPlanetEngine
from engines.vedic.house_engine import VedicHouseEngine
from engines.vedic.house_lord_engine import VedicHouseLordEngine
from engines.vedic.drishti_engine import VedicDrishtiEngine
from engines.vedic.strength_engine import VedicStrengthEngine
from domain.chart import ChartPlanet


class VedicEngine(IAstrologyEngine):
    """
    Vedic Core Calculation Engine.

    Sub-engines:
        - VedicPlanetEngine: Placed ChartPlanet calculation.
        - VedicHouseEngine: Cusps and occupant mappings.
        - VedicHouseLordEngine: Sign ownership and house lord placements.
        - VedicDrishtiEngine: Graha Drishti aspects.
        - VedicStrengthEngine: Dignities, combustion, retrograde, and strength scores.
    """

    def __init__(self) -> None:
        self.planet_engine = VedicPlanetEngine()
        self.house_engine = VedicHouseEngine()
        self.house_lord_engine = VedicHouseLordEngine()
        self.drishti_engine = VedicDrishtiEngine()
        self.strength_engine = VedicStrengthEngine()

    @property
    def engine_id(self) -> str:
        return "vedic"

    @property
    def version(self) -> str:
        return "2.0.0"

    def calculate(self, context: CalculationContext) -> Dict[str, Any]:
        """
        Executes Vedic calculation using single source of truth AstronomicalState.
        """
        if not context.astronomical_state:
            raise ValueError("CalculationContext is missing AstronomicalState.")

        # 1. Planet Engine: Map planets to house placements
        chart_planets: List[ChartPlanet] = self.planet_engine.calculate_chart_planets(context)

        # 2. House Engine: Cusps and occupants
        house_res = self.house_engine.calculate_houses_and_occupants(context, chart_planets)

        # 3. House Lord Engine: Sign ownership & lord positions
        lord_res = self.house_lord_engine.calculate_house_lords(
            context.astronomical_state.houses,
            chart_planets,
        )

        # 4. Graha Drishti Engine: Planetary aspects
        drishti_res = self.drishti_engine.calculate_graha_drishti(chart_planets)

        # 5. Strength Engine: Dignities & Scores
        strength_res = self.strength_engine.calculate_strengths_and_scores(chart_planets)

        # Enrich ChartPlanet objects with dignity & strength score
        dignity_map = {s["planet"]: s["strength"] for s in strength_res["strengths"]}
        enriched_chart_planets: List[ChartPlanet] = []
        for p in chart_planets:
            p.dignity = dignity_map.get(p.name, None)
            p.strength_score = strength_res["scores"].get(p.name, 0)
            enriched_chart_planets.append(p)

        return {
            "engine_id": self.engine_id,
            "version": self.version,
            "houses": house_res["houses"],
            "house_lords": lord_res["house_lords"],
            "house_lord_positions": lord_res["house_lord_positions"],
            "house_occupants": house_res["house_occupants"],
            "graha_drishti": drishti_res,
            "planet_strengths": strength_res["strengths"],
            "planet_scores": strength_res["scores"],
            "planets": enriched_chart_planets,
        }
