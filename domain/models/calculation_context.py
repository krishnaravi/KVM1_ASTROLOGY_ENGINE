"""
Domain model representing the unified calculation envelope.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from domain.models.birth_data import BirthData
from domain.models.location import ResolvedLocation
from domain.models.timezone import TimezoneContext
from domain.models.time_context import JulianDayContext
from domain.models.ephemeris_context import EphemerisContext
from domain.models.astronomical_state import AstronomicalState
from domain.models.stage_metrics import PipelineStageMetrics


@dataclass(frozen=True)
class CalculationContext:
    """
    Immutable calculation envelope flowing through the entire processing pipeline.

    Carries request trace ID, birth input, resolved location, timezone context,
    Julian Day context, ephemeris metadata, and the Single Source of Truth astronomical state.

    Attributes:
        trace_id: Unique UUID string identifying this calculation request execution.
        birth_data: Raw input birth details provided by client.
        resolved_location: Resolved geographic location.
        timezone_context: Resolved timezone and DST details.
        julian_day_context: Computed local, UTC, and Julian Day values.
        ephemeris_context: Swiss Ephemeris configuration metadata.
        astronomical_state: Computed astronomical state (Single Source of Truth).
        schema_version: Version string of the CalculationContext schema (default '1.0.0').
        pipeline_version: Version string of the active pipeline (default '2.0.0').
        context_version: Integer version counter incremented on stage transformations.
        stage_metrics: Tuple/List of PipelineStageMetrics records for audit tracking.
        engine_metadata: Optional dictionary for engine execution state and diagnostics.
    """
    trace_id: str
    birth_data: BirthData
    resolved_location: Optional[ResolvedLocation] = None
    timezone_context: Optional[TimezoneContext] = None
    julian_day_context: Optional[JulianDayContext] = None
    ephemeris_context: Optional[EphemerisContext] = None
    astronomical_state: Optional[AstronomicalState] = None
    schema_version: str = "1.0.0"
    pipeline_version: str = "2.0.0"
    context_version: int = 0
    stage_metrics: List[PipelineStageMetrics] = field(default_factory=list)
    engine_metadata: Dict[str, Any] = field(default_factory=dict)

    def with_enrichment(
        self,
        resolved_location: Optional[ResolvedLocation] = None,
        timezone_context: Optional[TimezoneContext] = None,
        julian_day_context: Optional[JulianDayContext] = None,
        ephemeris_context: Optional[EphemerisContext] = None,
        astronomical_state: Optional[AstronomicalState] = None,
        new_metric: Optional[PipelineStageMetrics] = None,
    ) -> 'CalculationContext':
        """
        Immutably produces a new CalculationContext instance with enriched fields,
        incremented context_version, and appended stage metrics.
        """
        metrics = list(self.stage_metrics)
        if new_metric:
            metrics.append(new_metric)

        return CalculationContext(
            trace_id=self.trace_id,
            birth_data=self.birth_data,
            resolved_location=resolved_location or self.resolved_location,
            timezone_context=timezone_context or self.timezone_context,
            julian_day_context=julian_day_context or self.julian_day_context,
            ephemeris_context=ephemeris_context or self.ephemeris_context,
            astronomical_state=astronomical_state or self.astronomical_state,
            schema_version=self.schema_version,
            pipeline_version=self.pipeline_version,
            context_version=self.context_version + 1,
            stage_metrics=metrics,
            engine_metadata=dict(self.engine_metadata),
        )
