from fastapi import APIRouter
from services.lagna_service import get_lagna

router = APIRouter(prefix="/api", tags=["Lagna"])


@router.get("/lagna")
def lagna(
    date: str,
    time: str,
    latitude: float,
    longitude: float
):
    return {
        "status": "success",
        "lagna": get_lagna(
            date,
            time,
            latitude,
            longitude
        )
    }