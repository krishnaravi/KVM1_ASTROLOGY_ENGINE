"""
House Lord Service
Parashari Rasi House Lords
"""

RASI_LORDS = {
    "மேஷம்": "Mars",
    "ரிஷபம்": "Venus",
    "மிதுனம்": "Mercury",
    "கடகம்": "Moon",
    "சிம்மம்": "Sun",
    "கன்னி": "Mercury",
    "துலாம்": "Venus",
    "விருச்சிகம்": "Mars",
    "தனுசு": "Jupiter",
    "மகரம்": "Saturn",
    "கும்பம்": "Saturn",
    "மீனம்": "Jupiter",
}


def get_house_lords(houses):
    """
    Input:
        Houses List

    Output:
        House + Sign + Lord
    """

    result = []

    for house in houses:

        result.append({
            "house": house["house"],
            "sign": house["sign"],
            "lord": RASI_LORDS[house["sign"]]
        })

    return result
