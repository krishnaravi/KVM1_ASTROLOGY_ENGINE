"""
Calculation Audit Logging Service implementing IAuditLogger.
"""

import json
import logging
from typing import Dict, Any, List
from core.interfaces.audit_interface import IAuditLogger
from domain.models.audit_log import CalculationAuditLog
from domain.models.calculation_context import CalculationContext
from domain.versioning import ENGINE_METADATA

logger = logging.getLogger("kvm1.audit")


class AuditLoggingService(IAuditLogger):
    """
    Structured logger recording immutable calculation lineage for reproducibility.
    """

    def __init__(self) -> None:
        self._logs: List[CalculationAuditLog] = []

    def log_calculation(self, audit_log: CalculationAuditLog) -> None:
        """
        Records an audit log entry in structured format.
        """
        self._logs.append(audit_log)
        log_payload = {
            "trace_id": audit_log.trace_id,
            "timestamp": audit_log.timestamp,
            "api_version": audit_log.api_version,
            "engine_version": audit_log.engine_version,
            "rule_version": audit_log.rule_version,
            "ephemeris_version": audit_log.ephemeris_version,
            "input_data": audit_log.input_data,
            "resolved_location": audit_log.resolved_location,
            "timezone_info": audit_log.timezone_info,
            "time_info": audit_log.time_info,
            "execution_time_ms": audit_log.execution_time_ms,
            "metadata": audit_log.metadata,
        }
        logger.info(json.dumps(log_payload))

    def create_audit_log_from_context(
        self,
        context: CalculationContext,
        timestamp_str: str,
        total_time_ms: float
    ) -> CalculationAuditLog:
        """
        Factory helper to build a CalculationAuditLog directly from a finalized CalculationContext.
        """
        input_data = {
            "date": context.birth_data.date,
            "time": context.birth_data.time,
            "birth_place": context.birth_data.birth_place,
            "latitude": context.birth_data.latitude,
            "longitude": context.birth_data.longitude,
        }

        resolved_loc = {
            "name": context.resolved_location.resolved_name,
            "latitude": context.resolved_location.latitude,
            "longitude": context.resolved_location.longitude,
            "provider": context.resolved_location.provider,
        } if context.resolved_location else {}

        tz_info = {
            "iana_timezone": context.timezone_context.iana_timezone,
            "utc_offset": context.timezone_context.utc_offset,
            "is_dst": context.timezone_context.is_dst,
        } if context.timezone_context else {}

        time_info = {
            "local_datetime": context.julian_day_context.local_datetime,
            "utc_datetime": context.julian_day_context.utc_datetime,
            "julian_day": context.julian_day_context.julian_day,
        } if context.julian_day_context else {}

        stage_metrics_summary = [
            {
                "stage_id": m.stage_id,
                "execution_time_ms": m.execution_time_ms,
                "cache_hit": m.cache_hit,
                "status": m.status,
            }
            for m in context.stage_metrics
        ]

        return CalculationAuditLog(
            trace_id=context.trace_id,
            timestamp=timestamp_str,
            api_version=ENGINE_METADATA.api_version,
            engine_version=ENGINE_METADATA.engine_version,
            rule_version=ENGINE_METADATA.rule_version,
            ephemeris_version=context.ephemeris_context.ephemeris_version if context.ephemeris_context else ENGINE_METADATA.ephemeris_version,
            input_data=input_data,
            resolved_location=resolved_loc,
            timezone_info=tz_info,
            time_info=time_info,
            execution_time_ms=total_time_ms,
            metadata={"stage_metrics": stage_metrics_summary},
        )

    def get_logged_records(self) -> List[CalculationAuditLog]:
        """Returns in-memory audit logs for verification/testing."""
        return list(self._logs)
