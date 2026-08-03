"""
Moolatrikona Strength
"""

from services.config.dignities import MOOLATRIKONA


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        data = MOOLATRIKONA.get(planet.name)

        if data is None:
            continue

        sign, start_degree, end_degree = data

        if (
            planet.sign == sign
            and start_degree <= planet.degree_in_sign <= end_degree
        ):

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Moolatrikona",
                    "score": 90,
                    "reason": (
                        f"{planet.name} is in Moolatrikona "
                        f"({planet.sign} {planet.degree_in_sign:.2f}°)"
                    ),
                }
            )

    return strengths