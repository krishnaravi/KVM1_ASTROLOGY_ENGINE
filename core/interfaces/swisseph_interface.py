"""
Abstract interface contract for Swiss Ephemeris wrapper.
"""

from abc import ABC, abstractmethod
from typing import Tuple


class ISwissephService(ABC):
    """
    Abstract Base Class defining the contract for Swiss Ephemeris astronomical calculations.
    Swiss Ephemeris is the Single Source of Truth for planetary positions.
    """

    @abstractmethod
    def calc_planet(self, julian_day: float, planet_id: int) -> Tuple[float, float, float]:
        """
        Calculates raw planetary position for a given Julian Day and planet ID.

        Args:
            julian_day: Astronomical Julian Day number in UT.
            planet_id: Swiss Ephemeris planet constant ID (e.g. SE_SUN = 0).

        Returns:
            Tuple of (longitude, latitude, speed).
        """
        pass

    @abstractmethod
    def get_ayanamsa(self, julian_day: float) -> float:
        """
        Retrieves the sidereal ayanamsa value in degrees for a given Julian Day.

        Args:
            julian_day: Astronomical Julian Day number in UT.

        Returns:
            Ayanamsa value in decimal degrees.
        """
        pass

    @abstractmethod
    def get_ephemeris_version(self) -> str:
        """
        Returns the version string of the active Swiss Ephemeris library.
        """
        pass
