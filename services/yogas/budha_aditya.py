"""
Budha Aditya Yoga
Sun + Mercury Conjunction
"""


def check(chart):

    planets = chart["planets"]

    sun = None
    mercury = None

    for planet in planets:

        if planet.name == "Sun":
            sun = planet

        elif planet.name == "Mercury":
            mercury = planet

    if sun is None or mercury is None:
        return None

    if sun.house != mercury.house:
        return None

    return {
        "name": "Budha Aditya Yoga",
        "found": True,
        "strength": "Normal",
        "house": sun.house,
        "reason": f"Sun and Mercury are conjunct in House {sun.house}"
    }