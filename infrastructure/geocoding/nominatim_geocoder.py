"""
OpenStreetMap Nominatim HTTP API Geocoder Adapter.
"""

import json
import urllib.parse
import urllib.request
from infrastructure.geocoding.base_geocoder import BaseGeocoder
from domain.models.location import ResolvedLocation


class NominatimGeocoder(BaseGeocoder):
    """
    Geocoding adapter using OpenStreetMap Nominatim API.
    """

    def __init__(
        self,
        timeout_seconds: float = 3.0,
        max_retries: int = 2,
    ) -> None:
        super().__init__(timeout_seconds=timeout_seconds, max_retries=max_retries)

    def geocode(self, place_name: str) -> ResolvedLocation:
        def _fetch() -> ResolvedLocation:
            encoded_query = urllib.parse.quote(place_name)
            url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"
            req = urllib.request.Request(url, headers={"User-Agent": "KVM1-AstrologyEngine/2.0"})

            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if not data or not isinstance(data, list):
                raise ValueError(f"Nominatim found no results for query '{place_name}'")

            item = data[0]
            lat = float(item["lat"])
            lon = float(item["lon"])
            display_name = item.get("display_name", place_name)

            return ResolvedLocation(
                resolved_name=display_name,
                latitude=lat,
                longitude=lon,
                provider="NominatimGeocoder",
            )

        return self.execute_with_retry(_fetch, provider_name="NominatimGeocoder")
