"""
Dhana Yoga Wealth Lord Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class DhanaYogaWealthLordRule(IRule):
    """
    Dhana Yoga rule evaluating association between 2nd lord (wealth) and 11th lord (gains).
    """

    @property
    def rule_id(self) -> str: return "RULE_DHANA_YOGA_2_11"
    @property
    def name(self) -> str: return "2nd-11th Lord Dhana Yoga Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Triggered when 2nd house lord and 11th house lord are conjoined."
    @property
    def priority(self) -> int: return 250
    @property
    def category(self) -> str: return "dhana_yoga"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        house_lords = engine_outputs.get("house_lords", {}) if engine_outputs else {}
        lord_positions = engine_outputs.get("house_lord_positions", {}) if engine_outputs else {}

        lord_2 = house_lords.get(2)
        lord_11 = house_lords.get(11)
        pos_2 = lord_positions.get(2)
        pos_11 = lord_positions.get(11)

        triggered = (pos_2 is not None and pos_11 is not None and pos_2 == pos_11)

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.92 if triggered else 0.0,
            payload={
                "lord_2nd": lord_2,
                "lord_11th": lord_11,
                "conjoined_house": pos_2 if triggered else None,
            },
            rule_version=self.version,
            priority=self.priority,
        )
