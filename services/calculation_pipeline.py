"""
Pure Pipeline Orchestrator for KVM1 Astrology Engine.
Must NOT contain astronomical calculations or business rules directly.
Only coordinates IPipelineStage services and handles CalculationContext state flow.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from core.interfaces.pipeline_interface import IPipelineStage
from core.interfaces.audit_interface import IAuditLogger
from domain.models.birth_data import BirthData
from domain.models.calculation_context import CalculationContext
from validators.birth_data_validator import BirthDataValidator
from core.errors import ValidationError, PipelineExecutionError
from services.audit_logging_service import AuditLoggingService


class CalculationPipeline:
    """
    Pure orchestrator driving CalculationContext through ordered IPipelineStage instances.
    """

    def __init__(
        self,
        stages: List[IPipelineStage],
        audit_logger: Optional[IAuditLogger] = None,
    ) -> None:
        self.stages: List[IPipelineStage] = stages
        self.audit_logger: Optional[IAuditLogger] = audit_logger or AuditLoggingService()

    def execute(
        self,
        birth_data: BirthData,
        trace_id: Optional[str] = None,
    ) -> CalculationContext:
        """
        Validates birth_data, constructs initial CalculationContext, and executes stages.

        Args:
            birth_data: Unvalidated BirthData input.
            trace_id: Optional trace UUID string (generated if omitted).

        Returns:
            Finalized CalculationContext containing Single Source of Truth astronomical state.
        """
        pipeline_start = time.perf_counter()
        req_trace_id = trace_id or str(uuid.uuid4())

        # 1. Boundary Input Validation
        val_result = BirthDataValidator.validate(birth_data)
        if not val_result.is_valid:
            error_msg = "; ".join(val_result.errors)
            raise ValidationError(
                human_message=f"Birth input validation failed: {error_msg}",
                trace_id=req_trace_id,
            )

        # 2. State 0: Initial CalculationContext
        context = CalculationContext(
            trace_id=req_trace_id,
            birth_data=birth_data,
        )

        # 3. Execute Stages Sequentially
        for stage in self.stages:
            try:
                context = stage.process(context)
            except Exception as e:
                total_ms = (time.perf_counter() - pipeline_start) * 1000.0
                if isinstance(self.audit_logger, AuditLoggingService):
                    audit_rec = self.audit_logger.create_audit_log_from_context(
                        context=context,
                        timestamp_str=datetime.now(timezone.utc).isoformat(),
                        total_time_ms=total_ms,
                    )
                    self.audit_logger.log_calculation(audit_rec)
                raise e

        # 4. Finalize Audit Logging
        total_pipeline_ms = (time.perf_counter() - pipeline_start) * 1000.0
        if isinstance(self.audit_logger, AuditLoggingService):
            audit_rec = self.audit_logger.create_audit_log_from_context(
                context=context,
                timestamp_str=datetime.now(timezone.utc).isoformat(),
                total_time_ms=total_pipeline_ms,
            )
            self.audit_logger.log_calculation(audit_rec)

        return context
