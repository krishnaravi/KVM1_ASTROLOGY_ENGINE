"""
Vedic House Engine.
Processes house cusps and house occupant placements from AstronomicalState.
"""

from typing import List, Dict, Any
from domain.models.calculation_context import CalculationContext
from domain.chart import ChartPlanet
from domain.house import House


class VedicHouseEngine:
    """
    Sub-engine responsible for house cusps and occupant mappings.
    Reads exclusively from AstronomicalState.
    """

    def calculate_houses_and_occupants(
        self,
        context: CalculationContext,
        chart_planets: List[ChartPlanet]
    ) -> Dict[str, Any]:
        """
        Calculates 12 house cusps and maps occupants per house.
        """
        if not context.astronomical_state:
            raise ValueError("AstronomicalState is required for VedicHouseEngine calculation.")

        raw_houses: List[House] = context.astronomical_state.houses

        formatted_houses: List[Dict[str, Any]] = []
        occupants_map: Dict[int, List[str]] = {h: [] for h in range(1, 13)}

        for p in chart_planets:
            if 1 <= p.house <= 12:
                occupants_map[p.house].append(p.name)

        for h in sorted(raw_houses, key=lambda x: x.number):
            formatted_houses.append({
                "house": h.number,
                "longitude": h.longitude,
                "sign": h.sign,
                "degree": round(h.longitude % 30, 6),
                "occupants": occupants_map[h.number],
            })

        return {
            "houses": formatted_houses,
            "house_occupants": {f"house_{k}": v for k, v in occupants_map.items()},
        }
