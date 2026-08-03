from pydantic import BaseModel


class Planet(BaseModel):

    name: str

    longitude: float
    latitude: float = 0.0
    speed: float = 0.0
    retrograde: bool = False

    sign: str
    degree_in_sign: float

    nakshatra: str
    nakshatra_lord: str
    pada: int