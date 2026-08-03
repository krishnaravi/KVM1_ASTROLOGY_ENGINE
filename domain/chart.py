from dataclasses import dataclass


@dataclass
class ChartPlanet:
    """
    Planet as placed inside a horoscope.
    Extends Planet with astrological information.
    """

    # Identity
    name: str

    # Astronomy
    longitude: float
    latitude: float
    speed: float
    retrograde: bool

    # Zodiac
    sign: str
    degree_in_sign: float

    # Horoscope
    house: int

    # Nakshatra
    nakshatra: str
    nakshatra_lord: str
    pada: int

    # Optional astronomical data
    declination: float = 0.0

    # Strength / Dignity
    dignity: str | None = None
    strength_score: int = 0