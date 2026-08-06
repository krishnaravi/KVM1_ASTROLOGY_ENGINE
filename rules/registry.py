"""
Rule Registry for KVM1 Astrology Engine.
Manages registration, category grouping, and priority ordering of IRule implementations.
"""

from typing import Dict, List, Optional
from core.interfaces.rule_interface import IRule


class RuleRegistry:
    """
    Registry container for IRule implementations.
    """

    def __init__(self) -> None:
        self._rules: Dict[str, IRule] = {}

    def register(self, rule: IRule) -> None:
        """
        Registers an IRule implementation.
        """
        self._rules[rule.rule_id.lower()] = rule

    def get(self, rule_id: str) -> IRule:
        """
        Retrieves a rule by rule_id.

        Raises:
            KeyError: If rule_id is not registered.
        """
        key = rule_id.lower()
        if key not in self._rules:
            raise KeyError(f"Rule '{rule_id}' is not registered in RuleRegistry.")
        return self._rules[key]

    def is_registered(self, rule_id: str) -> bool:
        """Checks if rule_id is registered."""
        return rule_id.lower() in self._rules

    def get_by_category(self, category: str) -> List[IRule]:
        """Returns rules matching a specific category string, sorted by priority descending."""
        cat_lower = category.lower().strip()
        matched = [r for r in self._rules.values() if r.category.lower() == cat_lower]
        return sorted(matched, key=lambda r: r.priority, reverse=True)

    def list_all_rules(self) -> List[IRule]:
        """Returns all registered rules sorted by priority (highest priority first)."""
        return sorted(self._rules.values(), key=lambda r: r.priority, reverse=True)

    def list_rule_ids(self) -> List[str]:
        """Returns list of all registered rule IDs."""
        return list(self._rules.keys())


# Global Rule Registry Instance
rule_registry: RuleRegistry = RuleRegistry()


def bootstrap_rules(registry: Optional[RuleRegistry] = None) -> RuleRegistry:
    """
    Bootstraps standard rules into RuleRegistry.
    """
    target = registry or rule_registry

    from rules.classical.kendra_placement_rule import KendraPlacementRule
    from rules.yogas.budha_aditya_rule import BudhaAdityaYogaRule
    from rules.raja_yogas.kendra_kona_lord_rule import KendraKonaRajaYogaRule
    from rules.dhana_yogas.wealth_lord_rule import DhanaYogaWealthLordRule
    from rules.arishta.dusthana_affliction_rule import DusthanaAfflictionRule
    from rules.neecha_bhanga.neecha_bhanga_rule import NeechaBhangaRule
    from rules.functional_dignity.functional_benefic_rule import FunctionalDignityRule

    default_rules = [
        KendraPlacementRule(),
        BudhaAdityaYogaRule(),
        KendraKonaRajaYogaRule(),
        DhanaYogaWealthLordRule(),
        DusthanaAfflictionRule(),
        NeechaBhangaRule(),
        FunctionalDignityRule(),
    ]

    for rule in default_rules:
        if not target.is_registered(rule.rule_id):
            target.register(rule)

    return target
