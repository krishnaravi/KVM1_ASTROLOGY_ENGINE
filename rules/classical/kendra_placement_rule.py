"""
Classical Kendra Placement Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class KendraPlacementRule(IRule):
    """
    Classical rule evaluating planetary placements in Kendra houses (1, 4, 7, 10).
    Reads ONLY from CalculationContext / AstronomicalState.
    """

    @property
    def rule_id(self) -> str: return "RULE_CLASSICAL_KENDRA"
    @property
    def name(self) -> str: return "Kendra House Placement Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Evaluates planets placed in Kendra houses (1st, 4th, 7th, 10th)."
    @property
    def priority(self) -> int: return 100
    @property
    def category(self) -> str: return "classical"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        if not context.astronomical_state:
            return RuleResult(
                rule_id=self.rule_id, category=self.category, rule_name=self.name,
                triggered=False, confidence_score=0.0, payload={"reason": "No AstronomicalState"},
                rule_version=self.version, priority=self.priority,
            )

        kendra_houses = {1, 4, 7, 10}
        planets = engine_outputs.get("planets", []) if engine_outputs else []

        kendra_planets = [p.name if hasattr(p, "name") else p["name"] for p in planets if (hasattr(p, "house") and p.house in kendra_houses) or (isinstance(p, dict) and p.get("house") in kendra_houses)]

        triggered = len(kendra_planets) > 0
        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.9 if triggered else 0.0,
            payload={"kendra_planets": kendra_planets, "count": len(kendra_planets)},
            rule_version=self.version,
            priority=self.priority,
        )
