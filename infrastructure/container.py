"""
Lightweight, framework-independent Dependency Injection Container for KVM1 Astrology Engine.
Pure Python implementation supporting singleton and factory registration.
"""

from typing import Dict, Any, Type, Callable, Optional


class DependencyResolutionError(Exception):
    """Exception raised when a requested service dependency cannot be resolved."""
    pass


class Container:
    """
    Pure Python Dependency Injection Container.

    Supports:
        - Singleton registration (same instance returned on every resolve call).
        - Factory registration (new instance created on every resolve call).
        - Direct instance override (ideal for unit testing and mock injection).
    """

    def __init__(self) -> None:
        self._singletons: Dict[Any, Any] = {}
        self._factories: Dict[Any, Callable[['Container'], Any]] = {}
        self._instances: Dict[Any, Any] = {}

    def register_singleton(self, service_type: Any, instance: Any) -> None:
        """
        Registers an explicit concrete singleton instance for a service type or key.
        """
        self._singletons[service_type] = instance

    def register_factory(self, service_type: Any, factory: Callable[['Container'], Any]) -> None:
        """
        Registers a factory callable that constructs a new instance upon request.
        """
        self._factories[service_type] = factory

    def register_instance(self, service_type: Any, instance: Any) -> None:
        """
        Alias for registering an instance override (e.g. mock objects in unit tests).
        """
        self._instances[service_type] = instance

    def resolve(self, service_type: Type[Any]) -> Any:
        """
        Resolves an instance registered for the given service type interface.

        Order of resolution:
            1. Explicit instance override (_instances)
            2. Registered singleton (_singletons)
            3. Registered factory (_factories)
        """
        if service_type in self._instances:
            return self._instances[service_type]

        if service_type in self._singletons:
            return self._singletons[service_type]

        if service_type in self._factories:
            factory = self._factories[service_type]
            return factory(self)

        raise DependencyResolutionError(
            f"Service '{service_type}' is not registered in the DI Container."
        )

    def is_registered(self, service_type: Any) -> bool:
        """Checks if a service type is registered in the container."""
        return (
            service_type in self._instances
            or service_type in self._singletons
            or service_type in self._factories
        )

    def clear(self) -> None:
        """Resets all registered singletons, factories, and instance overrides."""
        self._singletons.clear()
        self._factories.clear()
        self._instances.clear()


# Global Container Instance for Application Bootstrapping
container: Container = Container()


def bootstrap_container(c: Optional[Container] = None) -> Container:
    """
    Registers default production/development implementation services in DI Container.
    """
    target = c or container

    from core.interfaces.geocoder_interface import IGeocoderProvider
    from core.interfaces.timezone_interface import ITimezoneService
    from core.interfaces.julian_day_interface import IJulianDayService
    from core.interfaces.swisseph_interface import ISwissephService
    from core.interfaces.audit_interface import IAuditLogger

    from infrastructure.geocoding.offline_geocoder import OfflineGeocoder
    from services.timezone_service import TimezoneService
    from services.julian_day_service import JulianDayService
    from services.swisseph_service import SwissephService
    from services.audit_logging_service import AuditLoggingService

    target.register_singleton(IGeocoderProvider, OfflineGeocoder())
    target.register_singleton(ITimezoneService, TimezoneService())
    target.register_singleton(IJulianDayService, JulianDayService())
    target.register_singleton(ISwissephService, SwissephService())
    target.register_singleton(IAuditLogger, AuditLoggingService())

    return target
