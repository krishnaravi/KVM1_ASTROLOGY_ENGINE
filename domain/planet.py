from dataclasses import dataclass


@dataclass
class Planet:
    name: str
    longitude: float
    sign: str
    degree_in_sign: float
    
    nakshatra: str = ""
    nakshatra_lord: str = ""
    pada: int = 0