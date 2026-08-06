"""
Composite Geocoder adapter implementing prioritized fallback chain.
Priority: Offline Database -> GeoNames -> OpenStreetMap (Nominatim) -> Google Maps
"""

import logging
from typing import List, Optional
from core.interfaces.geocoder_interface import IGeocoderProvider
from domain.models.location import ResolvedLocation
from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
from infrastructure.geocoding.geonames_geocoder import GeoNamesGeocoder
from infrastructure.geocoding.nominatim_geocoder import NominatimGeocoder
from infrastructure.geocoding.google_geocoder import GoogleMapsGeocoder

logger = logging.getLogger("kvm1.composite_geocoder")


class CompositeGeocoder(IGeocoderProvider):
    """
    Composite Geocoder managing a prioritized list of geocoding providers.
    Iterates sequentially through registered providers until one successfully resolves the location.
    """

    def __init__(self, providers: Optional[List[IGeocoderProvider]] = None) -> None:
        if providers:
            self.providers: List[IGeocoderProvider] = providers
        else:
            # Default production priority chain:
            # 1. Offline Database (Instant, zero latency)
            # 2. GeoNames
            # 3. OpenStreetMap Nominatim
            # 4. Google Maps
            self.providers = [
                OfflineGeocoder(),
                GeoNamesGeocoder(),
                NominatimGeocoder(),
                GoogleMapsGeocoder(),
            ]

    def geocode(self, place_name: str) -> ResolvedLocation:
        errors: List[str] = []

        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                result = provider.geocode(place_name)
                logger.info(f"Successfully resolved location '{place_name}' using provider '{provider_name}'")
                return result
            except Exception as e:
                msg = f"Provider '{provider_name}' failed for '{place_name}': {str(e)}"
                logger.warning(msg)
                errors.append(msg)

        raise ValueError(
            f"All geocoding providers failed for query '{place_name}'. Errors: {'; '.join(errors)}"
        )
