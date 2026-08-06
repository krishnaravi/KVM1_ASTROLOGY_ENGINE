"""
Varga Registry managing registration and retrieval of all 14 Divisional Chart calculators.
"""

from typing import Dict, List, Optional
from vargas.base import IVargaCalculator
from vargas.calculators import (
    D2HoraCalculator,
    D3DrekkanaCalculator,
    D7SaptamsaCalculator,
    D9NavamsaCalculator,
    D10DasamsaCalculator,
    D12DwadasamsaCalculator,
    D16ShodasamsaCalculator,
    D20VimsamsaCalculator,
    D24ChaturvimsamsaCalculator,
    D27BhamsaCalculator,
    D30TrimsamsaCalculator,
    D40KhavedamsaCalculator,
    D45AkshavedamsaCalculator,
    D60ShastiamsaCalculator,
)


class VargaRegistry:
    """
    Registry container for IVargaCalculator implementations.
    """

    def __init__(self) -> None:
        self._vargas: Dict[str, IVargaCalculator] = {}

    def register(self, varga: IVargaCalculator) -> None:
        """Registers an IVargaCalculator instance."""
        self._vargas[varga.varga_code.upper()] = varga

    def get(self, varga_code: str) -> IVargaCalculator:
        """
        Retrieves a varga calculator by code (e.g. 'D9').

        Raises:
            KeyError: If the requested varga_code is not registered.
        """
        key = varga_code.upper()
        if key not in self._vargas:
            raise KeyError(f"Varga Calculator '{varga_code}' is not registered in VargaRegistry.")
        return self._vargas[key]

    def is_registered(self, varga_code: str) -> bool:
        """Checks if a varga_code is registered."""
        return varga_code.upper() in self._vargas

    def list_vargas(self) -> List[str]:
        """Returns a list of all registered varga codes."""
        return list(self._vargas.keys())


# Global Varga Registry Instance
varga_registry: VargaRegistry = VargaRegistry()


def bootstrap_vargas(registry: Optional[VargaRegistry] = None) -> VargaRegistry:
    """
    Registers the 14 standard Parashari Varga Calculators in the registry.
    """
    target = registry or varga_registry

    all_calculators = [
        D2HoraCalculator(),
        D3DrekkanaCalculator(),
        D7SaptamsaCalculator(),
        D9NavamsaCalculator(),
        D10DasamsaCalculator(),
        D12DwadasamsaCalculator(),
        D16ShodasamsaCalculator(),
        D20VimsamsaCalculator(),
        D24ChaturvimsamsaCalculator(),
        D27BhamsaCalculator(),
        D30TrimsamsaCalculator(),
        D40KhavedamsaCalculator(),
        D45AkshavedamsaCalculator(),
        D60ShastiamsaCalculator(),
    ]

    for calc in all_calculators:
        if not target.is_registered(calc.varga_code):
            target.register(calc)

    return target
