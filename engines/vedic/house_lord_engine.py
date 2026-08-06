"""
Vedic House Lord Engine.
Determines house lords and house lord positions based on sign ownership.
"""

from typing import List, Dict, Any
from domain.chart import ChartPlanet
from domain.house import House


# Sign Lord Ownership Mapping
SIGN_LORDS: Dict[str, str] = {
    "மேஷம்": "Mars",
    "ரிஷபம்": "Venus",
    "மிதுனம்": "Mercury",
    "கடகம்": "Moon",
    "சிம்மம்": "Sun",
    "கன்னி": "Mercury",
    "துலாம்": "Venus",
    "விருச்சிகம்": "Mars",
    "தனுசு": "Jupiter",
    "மகரம்": "Saturn",
    "கும்பம்": "Saturn",
    "மீனம்": "Jupiter",
}

# Tamil Lord Names fallback
TAMIL_SIGN_LORDS: Dict[str, str] = {
    "மேஷம்": "செவ்வாய்",
    "ரிஷபம்": "சுக்கிரன்",
    "மிதுனம்": "புதன்",
    "கடகம்": "சந்திரன்",
    "சிம்மம்": "சூரியன்",
    "கன்னி": "புதன்",
    "துலாம்": "சுக்கிரன்",
    "விருச்சிகம்": "செவ்வாய்",
    "தனுசு": "குரு",
    "மகரம்": "சனி",
    "கும்பம்": "சனி",
    "மீனம்": "குரு",
}


class VedicHouseLordEngine:
    """
    Sub-engine responsible for Parashari sign ownership and house lord placement calculations.
    """

    def calculate_house_lords(
        self,
        houses: List[House],
        chart_planets: List[ChartPlanet]
    ) -> Dict[str, Any]:
        """
        Computes house lords for all 12 houses and maps their placed house numbers.
        """
        planet_house_map: Dict[str, int] = {p.name: p.house for p in chart_planets}

        house_lords: Dict[int, str] = {}
        house_lord_positions: Dict[int, int] = {}

        sorted_houses = sorted(houses, key=lambda h: h.number)
        for h in sorted_houses:
            lord = SIGN_LORDS.get(h.sign, "Sun")
            house_lords[h.number] = lord
            house_lord_positions[h.number] = planet_house_map.get(lord, h.number)

        return {
            "house_lords": house_lords,
            "house_lord_positions": house_lord_positions,
        }
