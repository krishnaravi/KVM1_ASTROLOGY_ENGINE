import swisseph as swe
from datetime import datetime, timedelta, timezone as dt_timezone

from core.constants import SIDEREAL_MODE

# Set Lahiri Ayanamsa once
swe.set_sid_mode(SIDEREAL_MODE)


def get_utc_datetime(date_str: str, time_str: str, timezone: float = 0.0) -> datetime:
    local_dt = datetime.fromisoformat(f"{date_str}T{time_str}")
    local_tz = dt_timezone(timedelta(hours=float(timezone)))
    return local_dt.replace(tzinfo=local_tz).astimezone(dt_timezone.utc)


def get_julian_day(date_str: str, time_str: str, timezone: float = 0.0) -> float:
    utc_dt = get_utc_datetime(date_str, time_str, timezone)

    return swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour
        + utc_dt.minute / 60.0
        + utc_dt.second / 3600.0
        + utc_dt.microsecond / 3600000000.0,
    )