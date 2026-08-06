"""
Domain model representing an immutable calculation audit log.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class CalculationAuditLog:
    """
    Immutable audit log entity capturing calculation lineage for 100% reproducibility.

    Attributes:
        trace_id: Unique trace UUID matching the calculation request.
        timestamp: ISO 8601 UTC timestamp of execution.
        api_version: Active API contract version.
        engine_version: Active engine version.
        rule_version: Active rule set version.
        ephemeris_version: Active Swiss Ephemeris version.
        input_data: Serialized birth input payload.
        resolved_location: Serialized location metadata.
        timezone_info: Serialized timezone and DST metadata.
        time_info: Serialized time and Julian Day metadata.
        execution_time_ms: Total computation runtime in milliseconds.
        metadata: Optional additional execution diagnostics.
    """
    trace_id: str
    timestamp: str
    api_version: str
    engine_version: str
    rule_version: str
    ephemeris_version: str
    input_data: Dict[str, Any]
    resolved_location: Dict[str, Any]
    timezone_info: Dict[str, Any]
    time_info: Dict[str, Any]
    execution_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)
