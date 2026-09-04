from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ResponseModel(BaseModel):
    model_config = ConfigDict(extra="allow", from_attributes=True)


class RootResponse(ResponseModel):
    engine: str
    status: str


class HealthResponse(ResponseModel):
    status: str


class PlanetResponse(ResponseModel):
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


class PlanetPositionsResponse(ResponseModel):
    status: str
    planet: list[PlanetResponse]


class LagnaValue(ResponseModel):
    name: str
    longitude: float
    sign: str
    degree_in_sign: float


class LagnaResponse(ResponseModel):
    status: str
    lagna: LagnaValue


class HouseValue(ResponseModel):
    house: int
    longitude: float
    sign: str
    degree_in_sign: float


class HousesResponse(ResponseModel):
    status: str
    houses: list[HouseValue]


class RasiLagnaValue(ResponseModel):
    longitude: float
    sign: str
    degree: float


class HouseLordValue(ResponseModel):
    house: int
    sign: str
    lord: str


class HouseLordPositionValue(HouseLordValue):
    lord_house: int
    lord_sign: str


class HouseOccupantsValue(ResponseModel):
    house: int
    occupants: list[str]


class ConjunctionValue(ResponseModel):
    house: int
    planets: list[str]
    count: int


class AspectValue(ResponseModel):
    house: int
    type: str


class GrahaDrishtiValue(ResponseModel):
    planet: str
    from_house: int
    aspects: list[AspectValue]


class YogaValue(ResponseModel):
    name: str
    found: Optional[bool] = None
    strength: Optional[str] = None
    house: Optional[int] = None
    score: Optional[int] = None
    reason: str


class PlanetStrengthValue(ResponseModel):
    planet: str
    strength: str
    score: int
    reason: str


class ChartPlanetValue(ResponseModel):
    name: str
    longitude: float
    latitude: float
    speed: float
    retrograde: bool
    sign: str
    degree_in_sign: float
    house: int
    nakshatra: str
    nakshatra_lord: str
    pada: int
    declination: float
    dignity: Optional[str] = None
    strength_score: int = 0


class RasiChartResponse(ResponseModel):
    houses: list[HouseValue]
    lagna: RasiLagnaValue
    house_lords: list[HouseLordValue]
    house_lord_positions: list[HouseLordPositionValue]
    house_occupants: list[HouseOccupantsValue]
    conjunctions: list[ConjunctionValue]
    graha_drishti: list[GrahaDrishtiValue]
    yogas: list[YogaValue]
    planet_strengths: list[PlanetStrengthValue]
    planet_scores: dict[str, int]
    planets: list[ChartPlanetValue]