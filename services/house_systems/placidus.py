import swisseph as swe
from datetime import datetime

from core.constants import ZODIAC_SIGNS


def calculate(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
):
    """
    Calculate Placidus House Cusps
    using Swiss Ephemeris (Sidereal Lahiri).
    """

    dt = datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M"
    )

    jd = swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0
    )

    swe.set_sid_mode(swe.SIDM_LAHIRI)

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