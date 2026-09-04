import swisseph as swe

from core.constants import ZODIAC_SIGNS
from core.swisseph_service import get_julian_day


def calculate(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    timezone: float = 0.0,
):
    """
    Calculate Placidus House Cusps
    using Swiss Ephemeris (Sidereal Lahiri).
    """

    jd = get_julian_day(date_str, time_str, timezone)

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'P',
        swe.FLG_SIDEREAL
    )

    houses = []

    for i in range(12):
        cusp = cusps[i]

        houses.append(
            {
                "house": i + 1,
                "longitude": round(cusp, 6),
                "sign": ZODIAC_SIGNS[int(cusp // 30)],
                "degree_in_sign": round(cusp % 30, 6),
            }
        )

    return houses