"""
Abstract interface contract for pipeline stages.
"""

from abc import ABC, abstractmethod
from domain.models.calculation_context import CalculationContext


class IPipelineStage(ABC):
    """
    Abstract Base Class for an individual pipeline processing stage.

    Every stage receives an immutable CalculationContext and returns an updated,
    enriched CalculationContext. Services MUST NOT communicate directly with each other,
    only through the pipeline context.
    """

    @property
    @abstractmethod
    def stage_id(self) -> str:
        """Unique identifier string for the pipeline stage (e.g. 'STAGE_LOCATION')."""
        pass

    @property
    @abstractmethod
    def stage_name(self) -> str:
        """Human-readable display name of the pipeline stage."""
        pass

    @abstractmethod
    def process(self, context: CalculationContext) -> CalculationContext:
        """
        Processes the input context and returns an enriched CalculationContext.

        Args:
            context: Input CalculationContext instance.

        Returns:
            New CalculationContext instance containing stage results & execution metrics.
        """
        pass
