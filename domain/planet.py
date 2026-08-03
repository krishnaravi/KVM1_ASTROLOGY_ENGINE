from dataclasses import dataclass


@dataclass
class Planet:
    """
    Raw planet data returned from Swiss Ephemeris.
    This model should NEVER contain house, dignity or score.
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

    # Nakshatra
    nakshatra: str
    nakshatra_lord: str
    pada: int