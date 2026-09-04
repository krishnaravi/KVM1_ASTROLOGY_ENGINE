"""
Gaja Kesari Yoga
"""


def check(chart):
    moon = None
    jupiter = None

    for planet in chart["planets"]:
        if planet.name == "Moon":
            moon = planet
        elif planet.name == "Jupiter":
            jupiter = planet

    if moon is None or jupiter is None:
        return []

    relative_house = ((jupiter.house - moon.house) % 12) + 1

    if relative_house not in {1, 4, 7, 10}:
        return []

    ordinal = {1: "1st", 4: "4th", 7: "7th", 10: "10th"}[relative_house]

    return [{
        "name": "Gaja Kesari Yoga",
        "found": True,
        "strength": "Normal",
        "house": jupiter.house,
        "reason": (
            f"Jupiter is in House {jupiter.house}, "
            f"{ordinal} from Moon in House {moon.house}"
        ),
    }]