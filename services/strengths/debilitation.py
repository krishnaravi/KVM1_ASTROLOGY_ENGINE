"""
Debilitation Strength
"""

from services.config.dignities import DEBILITATION_SIGNS


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