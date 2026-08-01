"""
Graha Drishti Engine

Parashari Graha Aspects
"""


def aspect_house(from_house: int, offset: int):
    return ((from_house + offset - 1) % 12) + 1


def get_graha_drishti(chart_planets):

    results = []

    for planet in chart_planets:

        aspects = []

        if planet.name in [
            "Sun",
            "Moon",
            "Mercury",
            "Venus",
        ]:

            aspects.append({
                "house": aspect_house(
                    planet.house,
                    6,
                ),
                "type": "7th"
            })

        results.append({

            "planet": planet.name,

            "from_house": planet.house,

            "aspects": aspects

        })

    return results