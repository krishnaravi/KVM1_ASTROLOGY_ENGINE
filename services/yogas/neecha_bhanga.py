"""
Neecha Bhanga Raja Yoga
"""

from services.config.dignities import DEBILITATION_SIGNS
from services.house_lord_service import RASI_LORDS


KENDRA_HOUSES = {1, 4, 7, 10}

def check(chart):
    planets = chart.get("planets", [])
    planet_by_name = {planet.name: planet for planet in planets}
    yogas = []
    seen = set()

    for planet in planets:
        debilitated_sign = DEBILITATION_SIGNS.get(planet.name)

        if debilitated_sign is None or planet.sign != debilitated_sign:
            continue

        if planet.name in seen:
            continue

        sign_lord_name = RASI_LORDS.get(debilitated_sign)
        sign_lord = planet_by_name.get(sign_lord_name)

        if sign_lord is None or sign_lord.house not in KENDRA_HOUSES:
            continue

        seen.add(planet.name)
        yogas.append(
            {
                "name": "Neecha Bhanga Yoga",
                "found": True,
                "strength": "Normal",
                "house": sign_lord.house,
                "reason": (
                    f"{planet.name} is debilitated in {debilitated_sign}, "
                    f"but its sign lord {sign_lord_name} is placed in "
                    f"Kendra House {sign_lord.house}, causing Neecha Bhanga"
                ),
            }
        )

    return yogas