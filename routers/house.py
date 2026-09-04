from fastapi import APIRouter
from models.response_models import HousesResponse
from services.house_service import get_houses
from validators.api_input_validator import validate_api_inputs

router = APIRouter(prefix="/api", tags=["Houses"])


@router.get("/houses", response_model=HousesResponse)
def houses(
    date: str,
    time: str,
    latitude: float,
    longitude: float,
    timezone: float = 0.0,
):
    validate_api_inputs(
        date,
        time,
        latitude,
        longitude,
        timezone,
        require_location=True,
    )
    return {
        "status": "success",
        "houses": get_houses(
            date,
            time,
            latitude,
            longitude,
            timezone,
        )
    }