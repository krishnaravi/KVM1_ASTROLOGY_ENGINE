"""
Timezone Resolution Service implementing ITimezoneService and IPipelineStage.
"""

import time
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Optional

try:
    from timezonefinder import TimezoneFinder
    _TZ_FINDER: Optional[TimezoneFinder] = TimezoneFinder()
except ImportError:
    _TZ_FINDER = None

from core.interfaces.pipeline_interface import IPipelineStage
from core.interfaces.timezone_interface import ITimezoneService
from core.interfaces.cache_interface import ICacheProvider
from domain.models.calculation_context import CalculationContext
from domain.models.timezone import TimezoneContext
from domain.models.stage_metrics import PipelineStageMetrics
from core.errors import TimezoneResolutionError


class TimezoneService(ITimezoneService, IPipelineStage):
    """
    Service responsible for spatial lat/lon to IANA timezone & historical DST resolution.
    """

    def __init__(self, cache: Optional[ICacheProvider] = None) -> None:
        self.cache: Optional[ICacheProvider] = cache

    @property
    def stage_id(self) -> str:
        return "STAGE_TIMEZONE"

    @property
    def stage_name(self) -> str:
        return "Timezone Resolution Stage"

    def resolve_timezone(
        self,
        latitude: float,
        longitude: float,
        date_str: str,
        time_str: str,
    ) -> TimezoneContext:
        """
        Resolves spatial IANA timezone and historical offset/DST.
        """
        cache_key = f"tz:{latitude:.4f},{longitude:.4f}"

        iana_tz_name: Optional[str] = None

        if self.cache:
            cached = self.cache.get(cache_key)
            if isinstance(cached, str):
                iana_tz_name = cached

        if not iana_tz_name and _TZ_FINDER:
            try:
                iana_tz_name = _TZ_FINDER.timezone_at(lat=latitude, lng=longitude)
            except Exception:
                iana_tz_name = None

            if iana_tz_name and self.cache:
                self.cache.set(cache_key, iana_tz_name, ttl_seconds=86400)

        # Fallback if spatial lookup is unavailable
        if not iana_tz_name:
            iana_tz_name = "Asia/Kolkata" if (6.0 <= latitude <= 37.0 and 68.0 <= longitude <= 97.0) else "UTC"

        try:
            try:
                tz = ZoneInfo(iana_tz_name)
            except (ZoneInfoNotFoundError, Exception):
                if iana_tz_name.upper() == "UTC":
                    tz = timezone.utc
                elif "Kolkata" in iana_tz_name or "India" in iana_tz_name:
                    tz = timezone(timedelta(hours=5, minutes=30))
                else:
                    tz = timezone.utc

            # Parse local date and time
            time_parts = time_str.split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            second = int(time_parts[2]) if len(time_parts) > 2 else 0

            dt = datetime.strptime(date_str, "%Y-%m-%d").replace(
                hour=hour, minute=minute, second=second, tzinfo=tz
            )

            offset = dt.utcoffset()
            offset_seconds = int(offset.total_seconds()) if offset else 0

            # Formatter for human-readable offset (e.g. +05:30)
            sign = "+" if offset_seconds >= 0 else "-"
            abs_seconds = abs(offset_seconds)
            hours_off = abs_seconds // 3600
            mins_off = (abs_seconds % 3600) // 60
            utc_offset_str = f"{sign}{hours_off:02d}:{mins_off:02d}"

            is_dst = bool(dt.dst() and dt.dst().total_seconds() != 0)

            return TimezoneContext(
                iana_timezone=iana_tz_name,
                utc_offset=utc_offset_str,
                utc_offset_seconds=offset_seconds,
                is_dst=is_dst,
            )
        except Exception as e:
            raise TimezoneResolutionError(
                human_message=f"Failed to resolve timezone for ({latitude}, {longitude}): {str(e)}"
            ) from e

    def process(self, context: CalculationContext) -> CalculationContext:
        start_time = time.perf_counter()
        input_version = context.context_version

        if not context.resolved_location:
            raise TimezoneResolutionError(
                human_message="Cannot resolve timezone: ResolvedLocation is missing in CalculationContext.",
                trace_id=context.trace_id,
                stage_id=self.stage_id,
            )

        loc = context.resolved_location
        birth = context.birth_data

        try:
            tz_ctx = self.resolve_timezone(
                latitude=loc.latitude,
                longitude=loc.longitude,
                date_str=birth.date,
                time_str=birth.time,
            )
        except TimezoneResolutionError as tre:
            tre.trace_id = context.trace_id
            tre.stage_id = self.stage_id
            raise tre

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
            timezone_context=tz_ctx,
            new_metric=metric,
        )
