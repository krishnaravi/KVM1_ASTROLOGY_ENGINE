"""
Google Maps Geocoding HTTP API Adapter.
"""

import json
import urllib.parse
import urllib.request
from typing import Optional
from infrastructure.geocoding.base_geocoder import BaseGeocoder
from domain.models.location import ResolvedLocation


class GoogleMapsGeocoder(BaseGeocoder):
    """
    Geocoding adapter using Google Maps Geocoding API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout_seconds: float = 3.0,
        max_retries: int = 2,
    ) -> None:
        super().__init__(timeout_seconds=timeout_seconds, max_retries=max_retries)
        self.api_key: Optional[str] = api_key

    def geocode(self, place_name: str) -> ResolvedLocation:
        if not self.api_key:
            raise ValueError("GoogleMapsGeocoder requires a valid API key.")

        def _fetch() -> ResolvedLocation:
            encoded_query = urllib.parse.quote(place_name)
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_query}&key={self.api_key}"
            req = urllib.request.Request(url, headers={"User-Agent": "KVM1-AstrologyEngine/2.0"})

            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            results = data.get("results", [])
            if not results:
                raise ValueError(f"Google Maps found no results for query '{place_name}'")

            item = results[0]
            location = item["geometry"]["location"]
            lat = float(location["lat"])
            lon = float(location["lng"])
            formatted_address = item.get("formatted_address", place_name)

            return ResolvedLocation(
                resolved_name=formatted_address,
                latitude=lat,
                longitude=lon,
                provider="GoogleMapsGeocoder",
            )

        return self.execute_with_retry(_fetch, provider_name="GoogleMapsGeocoder")
