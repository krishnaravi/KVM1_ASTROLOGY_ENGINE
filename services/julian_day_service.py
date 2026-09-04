"""
Julian Day Calculation Service implementing IJulianDayService and IPipelineStage.
"""

import time
from core.swisseph_service import get_julian_day, get_utc_datetime
from core.interfaces.pipeline_interface import IPipelineStage
from core.interfaces.julian_day_interface import IJulianDayService
from domain.models.calculation_context import CalculationContext
from domain.models.time_context import JulianDayContext
from domain.models.timezone import TimezoneContext
from domain.models.stage_metrics import PipelineStageMetrics
from core.errors import JulianDayCalculationError


class JulianDayService(IJulianDayService, IPipelineStage):
    """
    Service responsible for converting local birth datetime into UTC datetime
    and computing Universal Time Julian Day.
    """

    @property
    def stage_id(self) -> str:
        return "STAGE_JULIAN_DAY"

    @property
    def stage_name(self) -> str:
        return "Julian Day Calculation Stage"

    def compute_julian_day(
        self,
        date_str: str,
        time_str: str,
        timezone_context: TimezoneContext,
    ) -> JulianDayContext:
        """
        Converts local datetime to UTC datetime and calculates Swiss Ephemeris Julian Day.
        """
        try:
            offset_hours = timezone_context.utc_offset_seconds / 3600.0
            utc_dt = get_utc_datetime(date_str, time_str, offset_hours)
            julian_day = float(get_julian_day(date_str, time_str, offset_hours))

            return JulianDayContext(
                local_datetime=f"{date_str}T{time_str}{timezone_context.utc_offset}",
                utc_datetime=utc_dt.isoformat(),
                julian_day=julian_day,
            )
        except Exception as e:
            raise JulianDayCalculationError(
                human_message=f"Failed to compute Julian Day for date='{date_str}' time='{time_str}': {str(e)}"
            ) from e

    def process(self, context: CalculationContext) -> CalculationContext:
        start_time = time.perf_counter()
        input_version = context.context_version

        if not context.timezone_context:
            raise JulianDayCalculationError(
                human_message="Cannot compute Julian Day: TimezoneContext is missing in CalculationContext.",
                trace_id=context.trace_id,
                stage_id=self.stage_id,
            )

        birth = context.birth_data
        tz_ctx = context.timezone_context

        try:
            jd_ctx = self.compute_julian_day(
                date_str=birth.date,
                time_str=birth.time,
                timezone_context=tz_ctx,
            )
        except JulianDayCalculationError as jde:
            jde.trace_id = context.trace_id
            jde.stage_id = self.stage_id
            raise jde

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metric = PipelineStageMetrics(
            stage_id=self.stage_id,
            stage_name=self.stage_name,
            input_context_version=input_version,
            output_context_version=input_version + 1,
            execution_time_ms=elapsed_ms,
            cache_hit=False,
            status="SUCCESS",
        )

        return context.with_enrichment(
            julian_day_context=jd_ctx,
            new_metric=metric,
        )
