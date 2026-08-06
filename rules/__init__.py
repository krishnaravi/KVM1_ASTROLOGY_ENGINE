"""
Rule Engine Package.
"""

from core.interfaces.rule_interface import IRule, IRuleEngine, RuleResult
from rules.registry import RuleRegistry, rule_registry, bootstrap_rules
from rules.rule_engine import RuleEngine

__all__ = [
    "IRule",
    "IRuleEngine",
    "RuleResult",
    "RuleRegistry",
    "rule_registry",
    "bootstrap_rules",
    "RuleEngine",
]
