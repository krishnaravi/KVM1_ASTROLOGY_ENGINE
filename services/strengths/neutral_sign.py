"""
Neutral Sign Strength
"""

from services.config.dignities import NEUTRAL_SIGNS


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        neutral_signs = NEUTRAL_SIGNS.get(
            planet.name,
            [],
        )

        if planet.sign in neutral_signs:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Neutral Sign",
                    "score": 55,
                    "reason": f"{planet.name} is in neutral sign {planet.sign}",
                }
            )

    return strengths