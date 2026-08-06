"""
Domain model representing execution metrics for a pipeline stage.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PipelineStageMetrics:
    """
    Immutable domain entity recording execution metrics for an individual pipeline stage.

    Attributes:
        stage_id: Unique stage identifier string (e.g. 'STAGE_LOCATION').
        stage_name: Human-readable display name of the stage.
        input_context_version: Version integer of CalculationContext prior to stage execution.
        output_context_version: Version integer of CalculationContext after stage execution.
        execution_time_ms: Runtime duration of the stage in milliseconds.
        cache_hit: Boolean flag indicating if result was resolved from cache.
        status: Execution status string ('SUCCESS' or 'FAILED').
        error_message: Optional error message string if stage failed.
    """
    stage_id: str
    stage_name: str
    input_context_version: int
    output_context_version: int
    execution_time_ms: float
    cache_hit: bool = False
    status: str = "SUCCESS"
    error_message: Optional[str] = None
