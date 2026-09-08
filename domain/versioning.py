"""
System version constants and immutable engine metadata for KVM1 Astrology Engine.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class EngineMetadata:
    """
    Immutable metadata describing the system version, ephemeris version,
    and default ayanamsa mode for KVM1 Astrology Engine.
    """
    api_version: str = "1.0.0"
    engine_version: str = "2.1.0"
    rule_version: str = "1.0.0"
    ephemeris_version: str = "Swiss Ephemeris 2.10.03"
    build_version: str = "2.1.0-build.1"
    ayanamsa: str = "Lahiri"


# Single immutable instance of EngineMetadata
ENGINE_METADATA: EngineMetadata = EngineMetadata()

# Backward-compatible convenience constants
API_VERSION: str = ENGINE_METADATA.api_version
ENGINE_VERSION: str = ENGINE_METADATA.engine_version
RULE_VERSION: str = ENGINE_METADATA.rule_version
EPHEMERIS_VERSION: str = ENGINE_METADATA.ephemeris_version
