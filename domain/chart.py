from dataclasses import dataclass


@dataclass
class ChartPlanet:
    name: str
    longitude: float
    sign: str
    degree_in_sign: float
    house: int
    nakshatra: str
    nakshatra_lord: str
    pada: int