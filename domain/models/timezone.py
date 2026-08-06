"""
Domain model representing timezone context.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimezoneContext:
    """
    Immutable domain entity representing resolved timezone and DST context.

    Attributes:
        iana_timezone: Standard IANA timezone string (e.g. 'Asia/Kolkata').
        utc_offset: Human-readable UTC offset string (e.g. '+05:30').
        utc_offset_seconds: Numeric UTC offset in seconds (e.g. 19800).
        is_dst: Boolean flag indicating if Daylight Saving Time was active.
    """
    iana_timezone: str
    utc_offset: str
    utc_offset_seconds: int
    is_dst: bool
