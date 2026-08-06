"""
Budha-Aditya Yoga Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class BudhaAdityaYogaRule(IRule):
    """
    Yoga rule evaluating conjunction of Sun and Mercury in the same house.
    """

    @property
    def rule_id(self) -> str: return "RULE_YOGA_BUDHA_ADITYA"
    @property
    def name(self) -> str: return "Budha-Aditya Yoga Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Triggered when Sun and Mercury are conjoined in the same house."
    @property
    def priority(self) -> int: return 200
    @property
    def category(self) -> str: return "yoga"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        planets = engine_outputs.get("planets", []) if engine_outputs else []

        sun = next((p for p in planets if (getattr(p, "name", None) or p.get("name")) == "Sun"), None)
        mercury = next((p for p in planets if (getattr(p, "name", None) or p.get("name")) == "Mercury"), None)

        if not sun or not mercury:
            return RuleResult(
                rule_id=self.rule_id, category=self.category, rule_name=self.name,
                triggered=False, confidence_score=0.0, payload={"reason": "Sun or Mercury missing"},
                rule_version=self.version, priority=self.priority,
            )

        sun_house = getattr(sun, "house", None) or sun.get("house")
        merc_house = getattr(mercury, "house", None) or mercury.get("house")

        triggered = (sun_house == merc_house and sun_house is not None)

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.95 if triggered else 0.0,
            payload={
                "sun_house": sun_house,
                "mercury_house": merc_house,
                "conjoined_house": sun_house if triggered else None,
            },
            rule_version=self.version,
            priority=self.priority,
        )
