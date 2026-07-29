from fastapi import APIRouter
from services.planet_service import get_all_planets

router = APIRouter(prefix="/api", tags=["Planets"])


@router.get("/planet-positions")
def planets_positions(date: str, time: str):
    return {
        "status": "success",
        "planet": get_all_planets(date, time)
    }