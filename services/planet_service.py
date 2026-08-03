import swisseph as swe

from core.constants import ZODIAC_SIGNS, PLANETS
from core.swisseph_service import get_julian_day
from core.nakshatra import get_nakshatra
from domain.planet import Planet


def get_planet_position(jd: float, planet_name: str, planet_id: int):

    result, _ = swe.calc_ut(
        jd,
        planet_id,
        swe.FLG_SIDEREAL | swe.FLG_SPEED,
    )

    longitude = result[0]
    latitude = result[1]
    speed = result[3]

    sign = ZODIAC_SIGNS[int(longitude // 30)]
    degree = longitude % 30

    nak = get_nakshatra(longitude)

    return Planet(
        name=planet_name,
        longitude=round(longitude, 6),
        latitude=round(latitude, 6),
        speed=round(speed, 6),
        retrograde=(speed < 0),
        sign=sign,
        degree_in_sign=round(degree, 6),
        nakshatra=nak["name"],
        nakshatra_lord=nak["lord"],
        pada=nak["pada"],
    )


def get_all_planets(date_str: str, time_str: str):

    jd = get_julian_day(date_str, time_str)

    planets = []

    for name, planet_id in PLANETS.items():

        planets.append(
            get_planet_position(
                jd,
                name,
                planet_id,
            )
        )

    rahu = next(
        p for p in planets
        if p.name == "Rahu"
    )

    ketu_longitude = (rahu.longitude + 180) % 360

    ketu_nak = get_nakshatra(
        ketu_longitude,
    )

    planets.append(

        Planet(
            name="Ketu",
            longitude=round(ketu_longitude, 6),
            latitude=0.0,
            speed=0.0,
            retrograde=False,
            sign=ZODIAC_SIGNS[int(ketu_longitude // 30)],
            degree_in_sign=round(ketu_longitude % 30, 6),
            nakshatra=ketu_nak["name"],
            nakshatra_lord=ketu_nak["lord"],
            pada=ketu_nak["pada"],
        )

    )

    return planets