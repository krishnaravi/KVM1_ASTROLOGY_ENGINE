"""
Rule Engine implementation of IRuleEngine.
Evaluates registered rules in priority order against CalculationContext and Engine outputs.
MUST NOT calculate astronomical positions.
"""

from typing import List, Dict, Any, Optional
from core.interfaces.rule_interface import IRuleEngine, IRule, RuleResult
from domain.models.calculation_context import CalculationContext
from rules.registry import RuleRegistry, rule_registry


class RuleEngine(IRuleEngine):
    """
    Dispatcher engine evaluating registered rules in priority order.
    """

    def __init__(self, registry: Optional[RuleRegistry] = None) -> None:
        self.registry: RuleRegistry = registry or rule_registry

    def register_rule(self, rule: IRule) -> None:
        """Registers a rule into the rule registry."""
        self.registry.register(rule)

    def evaluate_all(
        self,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> List[RuleResult]:
        """
        Evaluates all registered rules in descending priority order.
        """
        all_rules = self.registry.list_all_rules()
        results: List[RuleResult] = []

        for rule in all_rules:
            try:
                res = rule.evaluate(
                    context=context,
                    engine_outputs=engine_outputs,
                    varga_outputs=varga_outputs,
                )
                results.append(res)
            except Exception as e:
                # Wrap rule execution failures safely in a non-triggered RuleResult with error payload
                results.append(
                    RuleResult(
                        rule_id=rule.rule_id,
                        category=rule.category,
                        rule_name=rule.name,
                        triggered=False,
                        confidence_score=0.0,
                        payload={"error": str(e)},
                        rule_version=rule.version,
                        priority=rule.priority,
                    )
                )

        return results

    def evaluate_category(
        self,
        category: str,
        context: CalculationContext,
        engine_outputs: Optional[Dict[str, Any]] = None,
        varga_outputs: Optional[Dict[str, Any]] = None,
    ) -> List[RuleResult]:
        """
        Evaluates rules belonging to a specific category string.
        """
        cat_rules = self.registry.get_by_category(category)
        results: List[RuleResult] = []

        for rule in cat_rules:
            try:
                res = rule.evaluate(
                    context=context,
                    engine_outputs=engine_outputs,
                    varga_outputs=varga_outputs,
                )
                results.append(res)
            except Exception as e:
                results.append(
                    RuleResult(
                        rule_id=rule.rule_id,
                        category=rule.category,
                        rule_name=rule.name,
                        triggered=False,
                        confidence_score=0.0,
                        payload={"error": str(e)},
                        rule_version=rule.version,
                        priority=rule.priority,
                    )
                )

        return results
