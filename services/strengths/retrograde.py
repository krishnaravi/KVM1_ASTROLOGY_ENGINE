"""
Retrograde Strength
"""


def check(chart):

    strengths = []

    for planet in chart["planets"]:

        # Sun & Moon never become retrograde
        if planet.name in ("Sun", "Moon"):
            continue

        if planet.speed < 0:

            strengths.append(
                {
                    "planet": planet.name,
                    "strength": "Retrograde",
                    "score": 15,
                    "reason": (
                        f"{planet.name} is retrograde "
                        f"(speed {planet.speed:.4f})"
                    ),
                }
            )

    return strengths