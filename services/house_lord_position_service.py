"""
House Lord Position Service

Finds where each house lord is placed.
"""


def get_house_lord_positions(house_lords, planets):
    """
    Input:
        house_lords -> output of house_lord_service
        planets -> chart planets

    Output:
        House
        Sign
        Lord
        Lord House
        Lord Sign
    """

    result = []

    for house in house_lords:

        lord_name = house["lord"]

        lord_house = None
        lord_sign = None

        for planet in planets:

            if planet.name == lord_name:
                lord_house = planet.house
                lord_sign = planet.sign
                break

        result.append(
            {
                "house": house["house"],
                "sign": house["sign"],
                "lord": lord_name,
                "lord_house": lord_house,
                "lord_sign": lord_sign,
            }
        )

    return result