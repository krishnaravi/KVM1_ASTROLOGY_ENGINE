"""
Domain model representing the unified calculation envelope.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from domain.models.birth_data import BirthData
from domain.models.location import ResolvedLocation
from domain.models.timezone import TimezoneContext
from domain.models.time_context import JulianDayContext
from domain.models.ephemeris_context import EphemerisContext
from domain.models.astronomical_state import AstronomicalState


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
        engine_metadata: Optional dictionary for engine execution state and diagnostics.
    """
    trace_id: str
    birth_data: BirthData
    resolved_location: ResolvedLocation
    timezone_context: TimezoneContext
    julian_day_context: JulianDayContext
    ephemeris_context: EphemerisContext
    astronomical_state: Optional[AstronomicalState] = None
    engine_metadata: Dict[str, Any] = field(default_factory=dict)
