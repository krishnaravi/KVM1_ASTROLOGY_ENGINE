"""
Domain model representing the Single Source of Truth astronomical state.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from domain.planet import Planet
from domain.house import House


@dataclass(frozen=True)
class AstronomicalState:
    """
    Immutable Single Source of Truth astronomical calculation output from Swiss Ephemeris.

    Engines and rule evaluation modules MUST read directly from this state
    and NEVER re-compute astronomical longitudes or planetary positions.

    Attributes:
        julian_day: Astronomical Julian Day number in Universal Time.
        ayanamsa_deg: Sidereal ayanamsa value in degrees.
        planets: Tuple or list of calculated Planet entities.
        houses: Tuple or list of calculated House entities.
        additional_data: Optional dictionary for additional astronomical parameters.
    """
    julian_day: float
    ayanamsa_deg: float
    planets: List[Planet] = field(default_factory=list)
    houses: List[House] = field(default_factory=list)
    additional_data: Dict[str, Any] = field(default_factory=dict)
