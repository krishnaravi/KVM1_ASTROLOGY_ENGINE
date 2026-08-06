"""
Domain model representing time conversion context.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class JulianDayContext:
    """
    Immutable domain entity representing date/time conversion and Julian Day calculations.

    Attributes:
        local_datetime: ISO 8601 string of local birth date and time.
        utc_datetime: ISO 8601 string of converted UTC birth date and time.
        julian_day: Computed astronomical Julian Day number in Universal Time.
    """
    local_datetime: str
    utc_datetime: str
    julian_day: float
