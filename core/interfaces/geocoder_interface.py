"""
Abstract interface contract for Geocoder providers.
"""

from abc import ABC, abstractmethod
from domain.models.location import ResolvedLocation


class IGeocoderProvider(ABC):
    """
    Abstract Base Class defining the contract for geocoding service providers
    (Google Maps, Nominatim, GeoNames, Offline DB).
    """

    @abstractmethod
    def geocode(self, place_name: str) -> ResolvedLocation:
        """
        Resolves a location query string into a ResolvedLocation entity.

        Args:
            place_name: Location query string (e.g. 'Chennai, India').

        Returns:
            ResolvedLocation entity containing latitude, longitude, and provider name.

        Raises:
            ValueError: If the place cannot be found or resolved.
        """
        pass
