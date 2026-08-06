"""
Arishta Dusthana Affliction Rule.
"""

from typing import Dict, Any, Optional
from core.interfaces.rule_interface import IRule, RuleResult
from domain.models.calculation_context import CalculationContext


class DusthanaAfflictionRule(IRule):
    """
    Arishta rule evaluating natural malefics placed in Dusthana houses (6, 8, 12).
    """

    @property
    def rule_id(self) -> str: return "RULE_ARISHTA_DUSTHANA"
    @property
    def name(self) -> str: return "Dusthana House Affliction Rule"
    @property
    def version(self) -> str: return "1.0.0"
    @property
    def description(self) -> str: return "Triggered when natural malefics reside in 6th, 8th, or 12th house."
    @property
    def priority(self) -> int: return 150
    @property
    def category(self) -> str: return "arishta"

    def evaluate(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> RuleResult:
        malefics = {"Mars", "Saturn", "Rahu", "Ketu"}
        dusthana_houses = {6, 8, 12}

        planets = engine_outputs.get("planets", []) if engine_outputs else []
        afflicted: list = []

        for p in planets:
            name = getattr(p, "name", None) or p.get("name")
            house = getattr(p, "house", None) or p.get("house")
            if name in malefics and house in dusthana_houses:
                afflicted.append({"planet": name, "house": house})

        triggered = len(afflicted) > 0

        return RuleResult(
            rule_id=self.rule_id,
            category=self.category,
            rule_name=self.name,
            triggered=triggered,
            confidence_score=0.85 if triggered else 0.0,
            payload={"afflicted": afflicted, "count": len(afflicted)},
            rule_version=self.version,
            priority=self.priority,
        )
