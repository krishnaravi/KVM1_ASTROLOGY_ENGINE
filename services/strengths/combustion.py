"""
Combustion Strength
"""

from services.config.dignities import COMBUSTION_LIMITS


def angular_distance(a, b):
    d = abs(a - b)

    if d > 180:
        d = 360 - d

    return d


def check(chart):

    strengths = []

    sun = next(
        (p for p in chart["planets"] if p.name == "Sun"),
        None,
    )

    if sun is None:
        return strengths

    for planet in chart["planets"]:

        if planet.name == "Sun":
            continue

        limit = COMBUSTION_LIMITS.get(planet.name)

        if limit is None:
            continue

        distance = angular_distance(
            sun.longitude,
            planet.longitude,
        )

        if distance <= limit:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Combust",
                    "score": 25,
                    "reason": (
                        f"{planet.name} is combust "
                        f"({distance:.2f}° from Sun, limit {limit}°)"
                    ),
                }
            )

    return strengths