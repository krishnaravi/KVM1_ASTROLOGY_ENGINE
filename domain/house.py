"""
Domain model representing house cusps.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class House:
    """
    Immutable domain entity representing a house cusp placement.

    Attributes:
        number: House number (1 to 12).
        longitude: Longitude of house cusp in degrees (0.0 to 360.0).
        sign: Zodiac sign of house cusp.
    """
    number: int
    longitude: float
    sign: str