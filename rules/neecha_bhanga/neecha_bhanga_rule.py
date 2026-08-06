"""
Neecha Bhanga Raja Yoga Cancellation Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class NeechaBhangaRule(IRule):
    """
    Neecha Bhanga rule evaluating cancellation of debilitation for debilitated planets.
    """

    @property
    def rule_id(self) -> str: return "RULE_NEECHA_BHANGA"
    @property
    def name(self) -> str: return "Neecha Bhanga Cancellation Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Triggered when a debilitated planet has its debilitation cancelled (Neecha Bhanga)."
    @property
    def priority(self) -> int: return 350
    @property
    def category(self) -> str: return "neecha_bhanga"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        strengths = engine_outputs.get("planet_strengths", []) if engine_outputs else []
        planets = engine_outputs.get("planets", []) if engine_outputs else []

        debilitated_planets = [s["planet"] for s in strengths if s.get("strength") == "Debilitation"]
        if not debilitated_planets:
            return RuleResult(
                rule_id=self.rule_id, category=self.category, rule_name=self.name,
                triggered=False, confidence_score=0.0, payload={"reason": "No debilitated planets found"},
                rule_version=self.version, priority=self.priority,
            )

        kendra_houses = {1, 4, 7, 10}
        cancellations: list = []

        for deb_p in debilitated_planets:
            p_obj = next((p for p in planets if (getattr(p, "name", None) or p.get("name")) == deb_p), None)
            if p_obj:
                house = getattr(p_obj, "house", None) or p_obj.get("house")
                if house in kendra_houses:
                    cancellations.append({"planet": deb_p, "house": house, "reason": "Debilitated planet placed in Kendra from Lagna"})

        triggered = len(cancellations) > 0

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.95 if triggered else 0.0,
            payload={"cancellations": cancellations},
            rule_version=self.version,
            priority=self.priority,
        )
