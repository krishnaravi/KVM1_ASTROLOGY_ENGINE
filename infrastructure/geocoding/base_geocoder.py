"""
Base Geocoder class with built-in retry and timeout capabilities.
"""

import time
import logging
from typing import Callable, Optional
from core.interfaces.geocoder_interface import IGeocoderProvider
from domain.models.location import ResolvedLocation

logger = logging.getLogger("kvm1.geocoding")


class BaseGeocoder(IGeocoderProvider):
    """
    Abstract base class providing timeout and exponential backoff retry mechanics
    for geocoding providers.
    """

    def __init__(
        self,
        timeout_seconds: float = 3.0,
        max_retries: int = 2,
        backoff_factor: float = 0.5,
    ) -> None:
        self.timeout_seconds: float = timeout_seconds
        self.max_retries: int = max_retries
        self.backoff_factor: float = backoff_factor

    def execute_with_retry(
        self,
        func: Callable[[], ResolvedLocation],
        provider_name: str,
    ) -> ResolvedLocation:
        """
        Executes a geocoding callable with retries and exponential backoff.
        """
        last_exception: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                return func()
            except Exception as e:
                last_exception = e
                logger.warning(
                    f"Geocoder provider '{provider_name}' attempt {attempt}/{self.max_retries} failed: {str(e)}"
                )
                if attempt < self.max_retries:
                    time.sleep(self.backoff_factor * (2 ** (attempt - 1)))

        raise ValueError(
            f"Provider '{provider_name}' failed after {self.max_retries} attempts: {str(last_exception)}"
        ) from last_exception
