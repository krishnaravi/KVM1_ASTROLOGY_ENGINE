"""
Functional Benefic / Malefic Classification Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class FunctionalDignityRule(IRule):
    """
    Functional Benefic / Malefic rule classifying grahas based on Lagna sign ownership.
    """

    @property
    def rule_id(self) -> str: return "RULE_FUNCTIONAL_DIGNITY"
    @property
    def name(self) -> str: return "Functional Benefic/Malefic Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Classifies grahas as Functional Benefic, Malefic, or Neutral per Lagna sign."
    @property
    def priority(self) -> int: return 80
    @property
    def category(self) -> str: return "functional_dignity"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        house_lords = engine_outputs.get("house_lords", {}) if engine_outputs else {}
        if not house_lords:
            return RuleResult(
                rule_id=self.rule_id, category=self.category, rule_name=self.name,
                triggered=False, confidence_score=0.0, payload={"reason": "House lords missing"},
                rule_version=self.version, priority=self.priority,
            )

        # Lords of 1, 5, 9 are Functional Benefics (Kona lords)
        benefic_lords = {house_lords.get(1), house_lords.get(5), house_lords.get(9)} - {None}
        # Lords of 6, 8, 12 are Functional Malefics (Dusthana lords)
        malefic_lords = {house_lords.get(6), house_lords.get(8), house_lords.get(12)} - {None} - benefic_lords

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=True,
            confidence_score=1.0,
            payload={
                "functional_benefics": list(benefic_lords),
                "functional_malefics": list(malefic_lords),
            },
            rule_version=self.version,
            priority=self.priority,
        )
