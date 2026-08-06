"""
Core interfaces and abstract contracts for KVM1 Astrology Engine.
Pure Python abstract base classes adhering to Dependency Inversion Principle.
"""

from core.interfaces.geocoder_interface import IGeocoderProvider
from core.interfaces.cache_interface import ICacheProvider
from core.interfaces.timezone_interface import ITimezoneService
from core.interfaces.julian_day_interface import IJulianDayService
from core.interfaces.swisseph_interface import ISwissephService
from core.interfaces.engine_interface import IAstrologyEngine
from core.interfaces.rule_interface import IRule, RuleResult, IRuleEngine
from core.interfaces.audit_interface import IAuditLogger

__all__ = [
    "IGeocoderProvider",
    "ICacheProvider",
    "ITimezoneService",
    "IJulianDayService",
    "ISwissephService",
    "IAstrologyEngine",
    "IRule",
    "RuleResult",
    "IRuleEngine",
    "IAuditLogger",
]
