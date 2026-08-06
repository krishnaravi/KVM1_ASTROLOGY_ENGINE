"""
Engine Registry for KVM1 Astrology Engine.
Manages registration and lookup of pluggable IAstrologyEngine implementations.
"""

from typing import Dict, List, Optional
from core.interfaces.engine_interface import IAstrologyEngine


class EngineRegistry:
    """
    Registry container for pluggable astrology calculation engines.
    """

    def __init__(self) -> None:
        self._engines: Dict[str, IAstrologyEngine] = {}

    def register(self, engine: IAstrologyEngine) -> None:
        """
        Registers an IAstrologyEngine implementation.
        """
        self._engines[engine.engine_id.lower()] = engine

    def get(self, engine_id: str) -> IAstrologyEngine:
        """
        Retrieves a registered engine by engine_id.

        Raises:
            KeyError: If the requested engine_id is not registered.
        """
        key = engine_id.lower()
        if key not in self._engines:
            raise KeyError(f"Astrology Engine '{engine_id}' is not registered in EngineRegistry.")
        return self._engines[key]

    def is_registered(self, engine_id: str) -> bool:
        """Checks if an engine_id is registered."""
        return engine_id.lower() in self._engines

    def list_engines(self) -> List[str]:
        """Returns a list of all registered engine IDs."""
        return list(self._engines.keys())


# Global Engine Registry Instance
engine_registry: EngineRegistry = EngineRegistry()


def bootstrap_engines(registry: Optional[EngineRegistry] = None) -> EngineRegistry:
    """
    Bootstraps default system engines (VedicEngine) into EngineRegistry.
    """
    target = registry or engine_registry
    from engines.vedic.vedic_engine import VedicEngine

    if not target.is_registered("vedic"):
        target.register(VedicEngine())

    return target
