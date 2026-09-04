from fastapi import APIRouter
from models.response_models import PlanetPositionsResponse
from services.planet_service import get_all_planets
from validators.api_input_validator import validate_api_inputs

router = APIRouter(prefix="/api", tags=["Planets"])


@router.get("/planet-positions", response_model=PlanetPositionsResponse)
def planets_positions(date: str, time: str, timezone: float = 0.0):
    validate_api_inputs(date, time, timezone=timezone)
    return {
        "status": "success",
        "planet": get_all_planets(date, time, timezone)
    }