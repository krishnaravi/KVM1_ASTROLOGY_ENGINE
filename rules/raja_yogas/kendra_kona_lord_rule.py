"""
Raja Yoga Kendra-Kona Association Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class KendraKonaRajaYogaRule(IRule):
    """
    Raja Yoga rule evaluating association between Kendra lords (1, 4, 7, 10) and Kona lords (1, 5, 9).
    """

    @property
    def rule_id(self) -> str: return "RULE_RAJA_YOGA_KENDRA_KONA"
    @property
    def name(self) -> str: return "Kendra-Kona Raja Yoga Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Triggered when a Kendra lord and a Kona lord are conjoined in the same house."
    @property
    def priority(self) -> int: return 300
    @property
    def category(self) -> str: return "raja_yoga"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        house_lords = engine_outputs.get("house_lords", {}) if engine_outputs else {}
        lord_positions = engine_outputs.get("house_lord_positions", {}) if engine_outputs else {}

        if not house_lords or not lord_positions:
            return RuleResult(
                rule_id=self.rule_id, category=self.category, rule_name=self.name,
                triggered=False, confidence_score=0.0, payload={"reason": "House lords missing"},
                rule_version=self.version, priority=self.priority,
            )

        kendra_houses = [1, 4, 7, 10]
        kona_houses = [1, 5, 9]

        raja_yogas: list = []

        for ken in kendra_houses:
            ken_lord = house_lords.get(ken)
            ken_pos = lord_positions.get(ken)

            for kon in kona_houses:
                if ken == kon:
                    continue
                kon_lord = house_lords.get(kon)
                kon_pos = lord_positions.get(kon)

                if ken_pos and kon_pos and ken_pos == kon_pos:
                    raja_yogas.append({
                        "kendra_house": ken,
                        "kendra_lord": ken_lord,
                        "kona_house": kon,
                        "kona_lord": kon_lord,
                        "conjoined_house": ken_pos,
                    })

        triggered = len(raja_yogas) > 0

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.98 if triggered else 0.0,
            payload={"raja_yogas": raja_yogas, "count": len(raja_yogas)},
            rule_version=self.version,
            priority=self.priority,
        )
