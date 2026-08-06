"""
Domain model representing Swiss Ephemeris context.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EphemerisContext:
    """
    Immutable domain entity representing Swiss Ephemeris configuration metadata.

    Attributes:
        ephemeris_version: Version string of the active Swiss Ephemeris library.
        ayanamsa_name: Name of the active sidereal ayanamsa mode (e.g. 'Lahiri').
        ayanamsa_value: Numeric ayanamsa value in degrees for the given epoch.
    """
    ephemeris_version: str
    ayanamsa_name: str
    ayanamsa_value: float
