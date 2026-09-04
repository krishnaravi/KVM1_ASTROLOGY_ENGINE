from fastapi import APIRouter
from models.response_models import LagnaResponse
from services.lagna_service import get_lagna
from validators.api_input_validator import validate_api_inputs

router = APIRouter(prefix="/api", tags=["Lagna"])


@router.get("/lagna", response_model=LagnaResponse)
def lagna(
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
        "lagna": get_lagna(
            date,
            time,
            latitude,
            longitude,
            timezone,
        )
    }