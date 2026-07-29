import swisseph as swe
from datetime import datetime

swe.set_sid_mode(swe.SIDM_LAHIRI)

ZODIAC_SIGNS = [
    "மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்",
    "சிம்மம்", "கன்னி", "துலாம்", "விருச்சிகம்",
    "தனுசு", "மகரம்", "கும்பம்", "மீனம்"
]
def get_lagna(date_str: str, time_str: str, latitude: float, longitude: float):
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