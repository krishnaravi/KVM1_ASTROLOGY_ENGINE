"""
Abstract interface contract for Timezone Resolution service.
"""

from abc import ABC, abstractmethod
from domain.models.timezone import TimezoneContext


class ITimezoneService(ABC):
    """
    Abstract Base Class defining the contract for timezone & historical DST resolution.
    """

    @abstractmethod
    def resolve_timezone(
        self,
        latitude: float,
        longitude: float,
        date_str: str,
        time_str: str
    ) -> TimezoneContext:
        """
        Resolves IANA timezone, UTC offset, and DST status for given coordinates and datetime.

        Args:
            latitude: Geographic latitude in decimal degrees.
            longitude: Geographic longitude in decimal degrees.
            date_str: Local birth date in YYYY-MM-DD format.
            time_str: Local birth time in HH:MM or HH:MM:SS format.

        Returns:
            TimezoneContext entity.
        """
        pass
