"""
Own Sign Strength
"""

from services.config.dignities import OWN_SIGNS


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        own_signs = OWN_SIGNS.get(
            planet.name,
            [],
        )

        if planet.sign in own_signs:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Own Sign",
                    "score": 80,
                    "reason": f"{planet.name} is in its own sign {planet.sign}",
                }
            )

    return strengths