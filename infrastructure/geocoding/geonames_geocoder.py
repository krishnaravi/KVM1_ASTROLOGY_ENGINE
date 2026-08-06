"""
GeoNames HTTP API Geocoder Adapter.
"""

import json
import urllib.parse
import urllib.request
from typing import Optional
from infrastructure.geocoding.base_geocoder import BaseGeocoder
from domain.models.location import ResolvedLocation


class GeoNamesGeocoder(BaseGeocoder):
    """
    Geocoding adapter using the GeoNames Web Service API.
    """

    def __init__(
        self,
        username: str = "demo",
        timeout_seconds: float = 3.0,
        max_retries: int = 2,
    ) -> None:
        super().__init__(timeout_seconds=timeout_seconds, max_retries=max_retries)
        self.username: str = username

    def geocode(self, place_name: str) -> ResolvedLocation:
        def _fetch() -> ResolvedLocation:
            encoded_query = urllib.parse.quote(place_name)
            url = f"http://api.geonames.org/searchJSON?q={encoded_query}&maxRows=1&username={self.username}"
            req = urllib.request.Request(url, headers={"User-Agent": "KVM1-AstrologyEngine/2.0"})

            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            geonames = data.get("geonames", [])
            if not geonames:
                raise ValueError(f"GeoNames found no results for query '{place_name}'")

            item = geonames[0]
            lat = float(item["lat"])
            lon = float(item["lng"])
            name = f"{item.get('name', place_name)}, {item.get('countryName', '')}".strip(", ")

            return ResolvedLocation(
                resolved_name=name,
                latitude=lat,
                longitude=lon,
                provider="GeoNamesGeocoder",
            )

        return self.execute_with_retry(_fetch, provider_name="GeoNamesGeocoder")
