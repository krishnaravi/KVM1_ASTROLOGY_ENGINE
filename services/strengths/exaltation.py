"""
Exaltation Strength
"""

from services.config.dignities import EXALTATION_SIGNS


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        exalted_sign = EXALTATION_SIGNS.get(planet.name)

        if exalted_sign is None:
            continue

        if planet.sign == exalted_sign:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Exalted",
                    "score": 100,
                    "reason": f"{planet.name} is exalted in {planet.sign}",
                }
            )

    return strengths