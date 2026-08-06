"""
JSON Response Builder for KVM1 Astrology Engine.
Formats structured JSON API responses for prediction and report endpoints.
"""

from typing import Dict, Any


class JSONResponseBuilder:
    """
    Formats prediction and report outputs into standard API JSON payloads.
    """

    def build_response(
        self,
        prediction_payload: Dict[str, Any],
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Builds standardized final prediction JSON payload.
        """
        return {
            "status": "success",
            "summary": prediction_payload.get("summary", ""),
            "strengths": prediction_payload.get("strengths", []),
            "weaknesses": prediction_payload.get("weaknesses", []),
            "yogas": prediction_payload.get("yogas", []),
            "doshas": prediction_payload.get("doshas", []),
            "recommendations": prediction_payload.get("recommendations", []),
            "confidence_score": prediction_payload.get("confidence_score", 0.0),
            "trace_id": prediction_payload.get("trace_id", ""),
            "report": report_data,
        }
