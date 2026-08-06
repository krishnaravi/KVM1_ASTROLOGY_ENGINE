"""
Domain model representing a resolved geographic location.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedLocation:
    """
    Immutable domain entity representing a resolved geographic location.

    Attributes:
        resolved_name: Full display name of the resolved location.
        latitude: Geographic latitude in decimal degrees (-90.0 to +90.0).
        longitude: Geographic longitude in decimal degrees (-180.0 to +180.0).
        provider: Identifier of the geocoding provider used (default 'default').
    """
    resolved_name: str
    latitude: float
    longitude: float
    provider: str = "default"
