from typing import List

ZODIAC_SIGNS = [
    "மேஷம்",
    "ரிஷபம்",
    "மிதுனம்",
    "கடகம்",
    "சிம்மம்",
    "கன்னி",
    "துலாம்",
    "விருச்சிகம்",
    "தனுசு",
    "மகரம்",
    "கும்பம்",
    "மீனம்",
]


def calculate(lagna_longitude: float) -> List[dict]:
    """
    Whole Sign House System

    Input:
        lagna_longitude (0° - 360°)

    Output:
        [
            {
                "house": 1,
                "sign": "கன்னி",
                "sign_index": 5
            },
            ...
        ]
    """

    lagna_sign = int(lagna_longitude // 30)

    houses = []

    for i in range(12):
        sign_index = (lagna_sign + i) % 12

        houses.append(
            {
                "house": i + 1,
                "sign": ZODIAC_SIGNS[sign_index],
                "sign_index": sign_index,
            }
        )

    return houses