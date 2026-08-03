"""
Enemy Sign Strength
"""

from services.config.dignities import ENEMY_SIGNS


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        enemy_signs = ENEMY_SIGNS.get(
            planet.name,
            [],
        )

        if planet.sign in enemy_signs:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Enemy Sign",
                    "score": 40,
                    "reason": f"{planet.name} is in enemy sign {planet.sign}",
                }
            )

    return strengths