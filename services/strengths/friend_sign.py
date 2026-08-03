"""
Friend Sign Strength
"""

from services.config.dignities import FRIEND_SIGNS


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        friend_signs = FRIEND_SIGNS.get(
            planet.name,
            [],
        )

        if planet.sign in friend_signs:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Friend Sign",
                    "score": 70,
                    "reason": f"{planet.name} is in friend sign {planet.sign}",
                }
            )

    return strengths