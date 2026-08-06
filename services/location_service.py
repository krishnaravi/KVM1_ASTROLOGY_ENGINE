"""
Location Resolution Service implementing IPipelineStage.
"""

import time
from typing import Optional
from core.interfaces.pipeline_interface import IPipelineStage
from core.interfaces.geocoder_interface import IGeocoderProvider
from core.interfaces.cache_interface import ICacheProvider
from domain.models.calculation_context import CalculationContext
from domain.models.location import ResolvedLocation
from domain.models.stage_metrics import PipelineStageMetrics
from core.errors import LocationResolutionError


class LocationService(IPipelineStage):
    """
    Pipeline stage service responsible for resolving geographic location coordinates.
    Uses injected IGeocoderProvider and optional ICacheProvider.
    """

    def __init__(
        self,
        geocoder: IGeocoderProvider,
        cache: Optional[ICacheProvider] = None,
    ) -> None:
        self.geocoder: IGeocoderProvider = geocoder
        self.cache: Optional[ICacheProvider] = cache

    @property
    def stage_id(self) -> str:
        return "STAGE_LOCATION"

    @property
    def stage_name(self) -> str:
        return "Location Resolution Stage"

    def process(self, context: CalculationContext) -> CalculationContext:
        start_time = time.perf_counter()
        input_version = context.context_version
        cache_hit = False

        birth_data = context.birth_data

        # Scenario 1: Direct coordinates provided
        if birth_data.latitude is not None and birth_data.longitude is not None:
            resolved_name = birth_data.birth_place or f"({birth_data.latitude}, {birth_data.longitude})"
            resolved = ResolvedLocation(
                resolved_name=resolved_name,
                latitude=birth_data.latitude,
                longitude=birth_data.longitude,
                provider="DirectInput",
            )
        # Scenario 2: Birth place string provided
        elif birth_data.birth_place and birth_data.birth_place.strip():
            place = birth_data.birth_place.strip()
            cache_key = f"loc:{place.lower()}"

            if self.cache:
                cached = self.cache.get(cache_key)
                if cached and isinstance(cached, ResolvedLocation):
                    resolved = cached
                    cache_hit = True

            if not cache_hit:
                try:
                    resolved = self.geocoder.geocode(place)
                except Exception as e:
                    raise LocationResolutionError(
                        human_message=f"Failed to geocode location '{place}': {str(e)}",
                        trace_id=context.trace_id,
                        stage_id=self.stage_id,
                    ) from e

                if self.cache and resolved:
                    self.cache.set(cache_key, resolved, ttl_seconds=86400)
        else:
            raise LocationResolutionError(
                human_message="Neither 'birth_place' nor valid '(latitude, longitude)' coordinates were provided.",
                trace_id=context.trace_id,
                stage_id=self.stage_id,
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metric = PipelineStageMetrics(
            stage_id=self.stage_id,
            stage_name=self.stage_name,
            input_context_version=input_version,
            output_context_version=input_version + 1,
            execution_time_ms=elapsed_ms,
            cache_hit=cache_hit,
            status="SUCCESS",
        )

        return context.with_enrichment(
            resolved_location=resolved,
            new_metric=metric,
        )
