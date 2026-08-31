"""
Swiss Ephemeris foundation.

This module is the SINGLE canonical place where

    1. the Julian Day is computed, and
    2. the sidereal (ayanamsa) mode is configured.

No other module may call ``swe.julday()`` or ``swe.set_sid_mode()``.
Importing this module configures the ayanamsa exactly once, and every
module that needs a Julian Day imports ``get_julian_day`` from here --
so the ayanamsa is always configured before any ephemeris call.
"""

import swisseph as swe
from datetime import datetime

from core.constants import SIDEREAL_MODE

# Set Lahiri Ayanamsa once, at import time.
swe.set_sid_mode(SIDEREAL_MODE)


def get_julian_day(date_str: str, time_str: str) -> float:
    """
    Convert a ``YYYY-MM-DD`` date and ``HH:MM`` time to a Julian Day.

    The incoming wall-clock time is passed to Swiss Ephemeris exactly as
    given -- no timezone offset is applied and no UTC conversion is
    performed. That is deliberate and preserves the engine's existing
    behaviour; changing it is a separate, output-changing decision.

    Raises ``ValueError`` if the date or time does not match the format.
    """

    dt = datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M"
    )

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0
    )