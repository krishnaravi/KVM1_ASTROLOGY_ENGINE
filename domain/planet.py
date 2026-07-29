from dataclasses import dataclass


@dataclass
class Planet:
    name: str
    longitude: float
    sign: str
    degree_in_sign: float