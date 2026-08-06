"""
Offline Geocoder implementation of IGeocoderProvider for deterministic fast offline lookup.
"""

from typing import Dict, Tuple
from core.interfaces.geocoder_interface import IGeocoderProvider
from domain.models.location import ResolvedLocation


class OfflineGeocoder(IGeocoderProvider):
    """
    Offline Geocoder provider using an in-memory dictionary of major cities
    with fallback lookup.
    """

    KNOWN_CITIES: Dict[str, Tuple[float, float, str]] = {
        "chennai": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
        "mumbai": (19.0760, 72.8777, "Mumbai, Maharashtra, India"),
        "delhi": (28.6139, 77.2090, "New Delhi, Delhi, India"),
        "london": (51.5074, -0.1278, "London, Greater London, United Kingdom"),
        "new york": (40.7128, -74.0060, "New York City, New York, United States"),
        "sydney": (-33.8688, 151.2093, "Sydney, New South Wales, Australia"),
        "oslo": (59.9139, 10.7522, "Oslo, Norway"),
        "tokyo": (35.6762, 139.6503, "Tokyo, Japan"),
    }

    def geocode(self, place_name: str) -> ResolvedLocation:
        query = place_name.lower().strip()

        for key, (lat, lon, full_name) in self.KNOWN_CITIES.items():
            if key in query:
                return ResolvedLocation(
                    resolved_name=full_name,
                    latitude=lat,
                    longitude=lon,
                    provider="OfflineGeocoder",
                )

        # Fallback default lookup
        return ResolvedLocation(
            resolved_name=place_name.title(),
            latitude=13.0827,
            longitude=80.2707,
            provider="OfflineGeocoderFallback",
        )
