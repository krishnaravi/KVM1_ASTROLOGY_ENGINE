from dataclasses import dataclass


@dataclass
class BirthData:
    date: str
    time: str
    latitude: float
    longitude: float
    timezone: float = 5.5