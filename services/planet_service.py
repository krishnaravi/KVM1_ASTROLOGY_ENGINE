import swisseph as swe

from core.constants import ZODIAC_SIGNS, PLANETS
from core.swisseph_service import get_julian_day
from domain.planet import Planet


def get_planet_position(jd: float, planet_name: str, planet_id: int):
    result, _ = swe.calc_ut(
        jd,
        planet_id,
        swe.FLG_SIDEREAL
    )

    longitude = result[0]

    sign = ZODIAC_SIGNS[int(longitude // 30)]
    degree = longitude % 30

    return Planet(
        name=planet_name,
        longitude=round(longitude, 6),
        sign=sign,
        degree_in_sign=round(degree, 6)
    )


def get_all_planets(date_str: str, time_str: str):
    jd = get_julian_day(date_str, time_str)

    planets = []

    for name, planet_id in PLANETS.items():
        planets.append(
            get_planet_position(
                jd,
                name,
                planet_id
            )
        )

    # Rahu
    rahu = next(p for p in planets if p.name == "Rahu")

    # Ketu = Rahu + 180°
    ketu_longitude = (rahu.longitude + 180) % 360

    planets.append(
        Planet(
            name="Ketu",
            longitude=round(ketu_longitude, 6),
            sign=ZODIAC_SIGNS[int(ketu_longitude // 30)],
            degree_in_sign=round(ketu_longitude % 30, 6)
        )
    )

    return planets