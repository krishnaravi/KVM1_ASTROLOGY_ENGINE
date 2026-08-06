"""
Unified Exception Hierarchy for KVM1 Astrology Engine.
All system exceptions inherit from EngineError and carry trace_id, stage_id, error_code, and human_message.
"""

from typing import Optional


class EngineError(Exception):
    """
    Base Exception for all KVM1 Astrology Engine errors.
    """

    def __init__(
        self,
        human_message: str,
        error_code: str = "ENGINE_ERROR",
        trace_id: Optional[str] = None,
        stage_id: Optional[str] = None,
    ) -> None:
        super().__init__(human_message)
        self.human_message: str = human_message
        self.error_code: str = error_code
        self.trace_id: Optional[str] = trace_id
        self.stage_id: Optional[str] = stage_id

    def __str__(self) -> str:
        return f"[{self.error_code}] stage='{self.stage_id}' trace='{self.trace_id}': {self.human_message}"


class ValidationError(EngineError):
    """Raised when birth input boundary validation fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "VALIDATION",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="VALIDATION_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )


class LocationResolutionError(EngineError):
    """Raised when place geocoding fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "LOCATION_RESOLUTION",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="LOCATION_RESOLUTION_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )


class TimezoneResolutionError(EngineError):
    """Raised when spatial IANA timezone or DST lookup fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "TIMEZONE_RESOLUTION",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="TIMEZONE_RESOLUTION_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )


class JulianDayCalculationError(EngineError):
    """Raised when UTC conversion or Julian Day math fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "JULIAN_DAY_CALCULATION",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="JULIAN_DAY_CALCULATION_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )


class SwissEphemerisError(EngineError):
    """Raised when Swiss Ephemeris C-extension evaluation fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "SWISS_EPHEMERIS",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="SWISS_EPHEMERIS_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )


class PipelineExecutionError(EngineError):
    """Raised when pipeline stage execution or orchestration fails."""

    def __init__(
        self,
        human_message: str,
        trace_id: Optional[str] = None,
        stage_id: str = "PIPELINE_ORCHESTRATION",
    ) -> None:
        super().__init__(
            human_message=human_message,
            error_code="PIPELINE_EXECUTION_ERROR",
            trace_id=trace_id,
            stage_id=stage_id,
        )
