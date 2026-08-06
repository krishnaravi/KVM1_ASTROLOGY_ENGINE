"""
Prediction Engine for KVM1 Astrology Engine.
Synthesizes pre-computed outputs from RuleEngine, VedicEngine, VargaRegistry, and CalculationContext.
MUST NOT calculate astronomical positions.
"""

from typing import Dict, Any, List, Optional
from core.interfaces.rule_interface import RuleResult
from domain.models.calculation_context import CalculationContext
from predictions.explanation_engine import ExplanationEngine


class PredictionEngine:
    """
    Core Prediction Engine synthesizing pre-evaluated rule results and engine outputs.
    """

    def __init__(self, explanation_engine: Optional[ExplanationEngine] = None) -> None:
        self.explanations: ExplanationEngine = explanation_engine or ExplanationEngine()

    def generate_prediction(
        self,
        context: CalculationContext,
        rule_results: List[RuleResult],
        vedic_output: Optional[Dict[str, Any]] = None,
        varga_output: Optional[Dict[str, Any]] = None,
        lang: str = "ta",
    ) -> Dict[str, Any]:
        """
        Synthesizes rule outputs and engine context into structured prediction payload.
        """
        trace_id = context.trace_id if hasattr(context, "trace_id") and context.trace_id else "trace-default"

        strengths: List[Dict[str, Any]] = []
        weaknesses: List[Dict[str, Any]] = []
        yogas: List[Dict[str, Any]] = []
        doshas: List[Dict[str, Any]] = []
        recommendations: List[str] = []

        triggered_rule_ids: List[str] = []
        scores: List[float] = []

        for r in rule_results:
            if not r.triggered:
                continue

            triggered_rule_ids.append(r.rule_id)
            scores.append(r.confidence_score)
            explanation_text = self.explanations.explain_rule(r.rule_id, lang=lang)

            item = {
                "rule_id": r.rule_id,
                "category": r.category,
                "name": r.rule_name,
                "confidence": r.confidence_score,
                "description": explanation_text,
                "details": r.payload,
            }

            if r.category in ("yoga", "raja_yoga", "dhana_yoga", "neecha_bhanga"):
                yogas.append(item)
                strengths.append(item)
            elif r.category in ("arishta",):
                doshas.append(item)
                weaknesses.append(item)
            elif r.category in ("classical", "functional_dignity"):
                strengths.append(item)

        # Build recommendations
        if doshas:
            if lang.lower().startswith("ta"):
                recommendations.append("பாப கிரகங்களின் பாதிப்பை குறைக்க தினசரி காயத்ரி மந்திரம் மற்றும் வழிபாடு செய்யவும்.")
            else:
                recommendations.append("Perform daily planetary prayers and mantra recitations to mitigate malefic afflictions.")

        if yogas:
            if lang.lower().startswith("ta"):
                recommendations.append("சுப யோகங்களின் நற்பலன்களை பெற குலதெய்வ வழிபாடு மற்றும் அறச்செயல்களை தொடரவும்.")
            else:
                recommendations.append("Engage in spiritual and charitable activities to maximize the benefits of auspicious yogas.")

        # Aggregate overall confidence score
        overall_confidence = round(sum(scores) / len(scores), 2) if scores else 0.85

        summary_text = self.explanations.build_summary(triggered_rule_ids, lang=lang)

        return {
            "summary": summary_text,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "yogas": yogas,
            "doshas": doshas,
            "recommendations": recommendations,
            "confidence_score": overall_confidence,
            "trace_id": trace_id,
            "language": "ta" if lang.lower().startswith("ta") else "en",
        }
