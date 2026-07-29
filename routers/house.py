from fastapi import APIRouter
from services.house_service import get_houses

router = APIRouter(prefix="/api", tags=["Houses"])


@router.get("/houses")
def houses(
    date: str,
    time: str,
    latitude: float,
    longitude: float
):
    return {
        "status": "success",
        "houses": get_houses(
            date,
            time,
            latitude,
            longitude
        )
    }