import swisseph as swe

from core.constants import ZODIAC_SIGNS
from core.swisseph_service import get_julian_day

def get_lagna(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    timezone: float = 0.0,
):
    jd = get_julian_day(date_str, time_str, timezone)

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'P',
        swe.FLG_SIDEREAL
    )

    lagna_longitude = ascmc[0]

    return {
        "name": "Lagna",
        "longitude": round(lagna_longitude, 6),
        "sign": ZODIAC_SIGNS[int(lagna_longitude // 30)],
        "degree_in_sign": round(lagna_longitude % 30, 6)
    }