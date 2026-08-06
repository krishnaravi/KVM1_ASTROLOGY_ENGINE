"""
Abstract interface contract for Julian Day Calculation service.
"""

from abc import ABC, abstractmethod
from domain.models.time_context import JulianDayContext
from domain.models.timezone import TimezoneContext


class IJulianDayService(ABC):
    """
    Abstract Base Class defining the contract for converting local date/time into UTC Julian Day.
    """

    @abstractmethod
    def compute_julian_day(
        self,
        date_str: str,
        time_str: str,
        timezone_context: TimezoneContext
    ) -> JulianDayContext:
        """
        Converts local birth date/time into UTC datetime and computes the Universal Time Julian Day.

        Args:
            date_str: Local birth date in YYYY-MM-DD format.
            time_str: Local birth time in HH:MM or HH:MM:SS format.
            timezone_context: Resolved TimezoneContext entity.

        Returns:
            JulianDayContext entity.
        """
        pass
