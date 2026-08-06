"""
Abstract interface and base class for Divisional Chart (Varga) calculators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple
from domain.models.calculation_context import CalculationContext
from domain.planet import Planet
from core.constants import ZODIAC_SIGNS


class IVargaCalculator(ABC):
    """
    Abstract Base Class for a Divisional Chart (Varga) calculator.
    """

    @property
    @abstractmethod
    def varga_code(self) -> str:
        """Unique varga code e.g. 'D9', 'D10', 'D60'."""
        pass

    @property
    @abstractmethod
    def varga_name(self) -> str:
        """Human-readable varga name e.g. 'Navamsa', 'Dasamsa'."""
        pass

    @property
    @abstractmethod
    def division_factor(self) -> int:
        """Number of divisions per sign (e.g. 9 for D9)."""
        pass

    @abstractmethod
    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        """
        Calculates the varga sign name and degree within that varga sign for a given longitude.

        Args:
            longitude: Ecliptic longitude in degrees (0.0 to 360.0).

        Returns:
            Tuple of (varga_sign_name, degree_in_varga_sign).
        """
        pass

    def calculate_varga_chart(self, context: CalculationContext) -> Dict[str, Any]:
        """
        Calculates divisional chart placements for all planets and ascendant
        reading exclusively from AstronomicalState.
        """
        if not context.astronomical_state:
            raise ValueError("AstronomicalState is required for Varga calculation.")

        planets: List[Planet] = context.astronomical_state.planets
        ascendant_lon = context.astronomical_state.additional_data.get("ascendant_longitude", 0.0)

        # Calculate Varga Ascendant
        asc_sign, asc_deg = self.calculate_varga_sign(ascendant_lon)

        # Calculate Varga Planets
        varga_planets: List[Dict[str, Any]] = []
        for p in planets:
            v_sign, v_deg = self.calculate_varga_sign(p.longitude)
            varga_planets.append({
                "planet": p.name,
                "rashi_longitude": p.longitude,
                "varga_sign": v_sign,
                "varga_degree": round(v_deg, 6),
            })

        return {
            "varga_code": self.varga_code,
            "varga_name": self.varga_name,
            "division_factor": self.division_factor,
            "varga_ascendant": {
                "sign": asc_sign,
                "degree": round(asc_deg, 6),
            },
            "planets": varga_planets,
        }
