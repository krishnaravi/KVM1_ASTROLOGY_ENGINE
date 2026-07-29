from pydantic import BaseModel


class PlanetPosition(BaseModel):
    name: str
    longitude: float
    sign: str
    degree_in_sign: float