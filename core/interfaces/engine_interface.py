"""
Abstract interface contract for pluggable Astrology Engines.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.models.calculation_context import CalculationContext


class IAstrologyEngine(ABC):
    """
    Abstract Base Class for pluggable system calculation engines
    (Vedic Engine, KP Engine, Jaimini Engine, Nadi Engine, etc.).

    Engines consume the Single Source of Truth CalculationContext and MUST NOT
    recompute raw astronomical positions.
    """

    @property
    @abstractmethod
    def engine_id(self) -> str:
        """
        Unique identifier string for the engine (e.g. 'vedic', 'kp', 'jaimini').
        """
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Engine version string.
        """
        pass

    @abstractmethod
    def calculate(self, context: CalculationContext) -> Dict[str, Any]:
        """
        Executes engine-specific analysis using context.astronomical_state.

        Args:
            context: Immutable CalculationContext envelope.

        Returns:
            Dictionary containing engine calculation outputs.
        """
        pass
