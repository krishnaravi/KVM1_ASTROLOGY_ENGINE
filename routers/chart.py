from fastapi import APIRouter

from services.chart_service import build_rasi_chart

router = APIRouter(
    prefix="/api",
    tags=["Chart"]
)

@router.get("/rasi-chart")
def rasi_chart(
    date: str,
    time: str,
    latitude: float,
    longitude: float
):
    return build_rasi_chart(
        date,
        time,
        latitude,
        longitude
    )