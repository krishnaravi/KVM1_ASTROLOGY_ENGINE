"""
Report Builder for KVM1 Astrology Engine.
Assembles prediction findings into structured report sections.
"""

from typing import Dict, Any, List


class ReportBuilder:
    """
    Constructs structured astrological report sections from prediction data.
    Separates prediction calculation logic from presentation formatting.
    """

    def build_report_sections(self, prediction_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforms prediction payload into standardized report sections.
        """
        lang = prediction_payload.get("language", "ta")
        is_tamil = (lang == "ta")

        title = "கே.வி.எம்.1 ஜோதிட கணிப்பு அறிக்கை" if is_tamil else "KVM1 Astrology Calculation & Prediction Report"
        exec_summary = prediction_payload.get("summary", "")

        section_strengths = {
            "title": "நற்பலன்கள் மற்றும் யோக பலம்" if is_tamil else "Strengths & Auspicious Yogas",
            "items": [item["description"] for item in prediction_payload.get("strengths", [])],
        }

        section_weaknesses = {
            "title": "சவால்கள் மற்றும் பரிகார அமைப்புகள்" if is_tamil else "Afflictions & Vulnerabilities",
            "items": [item["description"] for item in prediction_payload.get("weaknesses", [])],
        }

        section_recommendations = {
            "title": "பரிந்துரைக்கப்படும் வழிபாடுகள்" if is_tamil else "Recommended Vedic Remedies",
            "items": prediction_payload.get("recommendations", []),
        }

        return {
            "title": title,
            "executive_summary": exec_summary,
            "sections": [
                section_strengths,
                section_weaknesses,
                section_recommendations,
            ],
            "metadata": {
                "confidence_score": prediction_payload.get("confidence_score", 0.0),
                "trace_id": prediction_payload.get("trace_id", ""),
                "language": lang,
            }
        }
