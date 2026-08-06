"""
Vedic Graha Drishti Engine.
Calculates Parashari planetary aspects (7th full aspect + Mars 4/8, Jupiter 5/9, Saturn 3/10).
"""

from typing import List, Dict, Any
from domain.chart import ChartPlanet


class VedicDrishtiEngine:
    """
    Sub-engine responsible for Graha Drishti (planetary aspect) calculations.
    """

    ASPECT_RULES: Dict[str, List[int]] = {
        "Sun": [7],
        "Moon": [7],
        "Mercury": [7],
        "Venus": [7],
        "Mars": [4, 7, 8],
        "Jupiter": [5, 7, 9],
        "Saturn": [3, 7, 10],
        "Rahu": [5, 7, 9],
        "Ketu": [5, 7, 9],
    }

    def calculate_graha_drishti(self, chart_planets: List[ChartPlanet]) -> Dict[str, List[int]]:
        """
        Calculates target aspected house numbers for each graha.
        """
        drishti_map: Dict[str, List[int]] = {}

        for p in chart_planets:
            offsets = self.ASPECT_RULES.get(p.name, [7])
            aspected_houses: List[int] = []

            for offset in offsets:
                # 1-indexed house wrapping: (house + offset - 1) % 12 + 1
                target_house = (p.house + offset - 1) % 12 + 1
                aspected_houses.append(target_house)

            drishti_map[p.name] = sorted(aspected_houses)

        return drishti_map
