import swisseph as swe
from datetime import datetime

from core.constants import SIDEREAL_MODE

# Set Lahiri Ayanamsa once
swe.set_sid_mode(SIDEREAL_MODE)


def get_julian_day(date_str: str, time_str: str) -> float:
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