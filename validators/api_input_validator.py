import re
from datetime import datetime
from typing import Optional

from fastapi import HTTPException


_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$")


def validate_api_inputs(
    date: str,
    time: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    timezone: float = 0.0,
    require_location: bool = False,
) -> None:
    errors = []

    if not _DATE_PATTERN.fullmatch(date) or not _is_valid_date(date):
        errors.append("date must be a valid date in YYYY-MM-DD format")

    if not _TIME_PATTERN.fullmatch(time):
        errors.append("time must use HH:MM or HH:MM:SS format")

    if require_location:
        if latitude is None:
            errors.append("latitude is required")
        elif not -90.0 <= latitude <= 90.0:
            errors.append("latitude must be between -90 and 90")

        if longitude is None:
            errors.append("longitude is required")
        elif not -180.0 <= longitude <= 180.0:
            errors.append("longitude must be between -180 and 180")

    if not -12.0 <= timezone <= 14.0:
        errors.append("timezone must be between -12 and 14")

    if errors:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Invalid calculation parameters",
                "errors": errors,
            },
        )


def _is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True