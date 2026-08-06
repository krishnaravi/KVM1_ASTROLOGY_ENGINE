"""
Abstract interface contract for Calculation Audit Logger.
"""

from abc import ABC, abstractmethod
from domain.models.audit_log import CalculationAuditLog


class IAuditLogger(ABC):
    """
    Abstract Base Class defining the contract for structured calculation audit logging.
    """

    @abstractmethod
    def log_calculation(self, audit_log: CalculationAuditLog) -> None:
        """
        Persists or outputs an immutable CalculationAuditLog record.

        Args:
            audit_log: CalculationAuditLog entity.
        """
        pass
