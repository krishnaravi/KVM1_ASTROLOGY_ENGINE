"""
House Occupants Service

Returns all planets occupying each house.
"""


def get_house_occupants(planets):
    result = []

    for house_no in range(1, 13):
        occupants = []

        for planet in planets:
            if planet.house == house_no:
                occupants.append(planet.name)

        result.append(
            {
                "house": house_no,
                "occupants": occupants,
            }
        )

    return result