"""
Domain model representing raw planetary astronomical data.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Planet:
    """
    Raw planet data calculated from Swiss Ephemeris.

    This model represents pure astronomical state and should NEVER contain
    horoscope house placements, dignities, or strength scores.

    Attributes:
        name: Name of the graha / planet (e.g. 'Sun', 'Moon', 'Mars').
        longitude: Tropical/sidereal ecliptic longitude in degrees (0.0 to 360.0).
        latitude: Ecliptic latitude in degrees.
        speed: Daily motion speed in degrees per day (negative indicates retrograde).
        retrograde: Boolean flag indicating if the planet is in retrograde motion.
        sign: Zodiac sign name (Tamil string key).
        degree_in_sign: Degree within the sign (0.0 to 30.0).
        nakshatra: Nakshatra name.
        nakshatra_lord: Lord of the Nakshatra.
        pada: Pada number (1 to 4).
    """
    name: str
    longitude: float
    latitude: float
    speed: float
    retrograde: bool
    sign: str
    degree_in_sign: float
    nakshatra: str
    nakshatra_lord: str
    pada: int