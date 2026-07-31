"""
Graha Conjunction Service

Detects planetary conjunctions based on house occupancy.
"""


def get_conjunctions(house_occupants):
    result = []

    for house in house_occupants:
        planets = house["occupants"]

        if len(planets) >= 2:
            result.append(
                {
                    "house": house["house"],
                    "planets": planets,
                    "count": len(planets),
                }
            )

    return result