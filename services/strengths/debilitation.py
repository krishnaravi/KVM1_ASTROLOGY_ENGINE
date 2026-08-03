"""
Debilitation Strength
"""

from services.config.dignities import DEBILITATION_SIGNS

DEBILITATION_SIGNS = {
    "Sun": "துலாம்",
    "Moon": "விருச்சிகம்",
    "Mars": "கடகம்",
    "Mercury": "மீனம்",
    "Jupiter": "மகரம்",
    "Venus": "கன்னி",
    "Saturn": "மேஷம்",
}


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        debilitated_sign = DEBILITATION_SIGNS.get(planet.name)

        if debilitated_sign is None:
            continue

        if planet.sign == debilitated_sign:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Debilitated",
                    "score": 20,
                    "reason": f"{planet.name} is debilitated in {planet.sign}",
                }
            )

    return strengths