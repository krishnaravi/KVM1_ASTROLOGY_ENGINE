"""
Domain model representing raw birth details.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BirthData:
    """
    Immutable domain entity representing raw birth details provided by the client.

    Attributes:
        date: Date of birth in YYYY-MM-DD format.
        time: Time of birth in HH:MM or HH:MM:SS format.
        birth_place: Optional name of birth place (e.g. 'Chennai, India').
        latitude: Optional geographic latitude (-90.0 to +90.0).
        longitude: Optional geographic longitude (-180.0 to +180.0).
        timezone: Optional numerical timezone offset (default 5.5 for IST).
    """
    date: str
    time: str
    birth_place: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[float] = 5.5
