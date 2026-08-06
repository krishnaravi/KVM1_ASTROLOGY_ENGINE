"""
Explanation Engine for KVM1 Astrology Engine.
Generates human-readable explanations for rules, yogas, and dignities in Tamil and English.
"""

from typing import Dict, Any, List


class ExplanationEngine:
    """
    Multilingual Explanation Engine (Tamil first, English supported).
    """

    TRANSLATIONS: Dict[str, Dict[str, str]] = {
        "RULE_CLASSICAL_KENDRA": {
            "ta": "கேந்திர வீடுகளில் (1, 4, 7, 10) கிரகங்கள் அமைந்துள்ளதால் ஜாதகத்திற்கு வலிமை கிடைக்கிறது.",
            "en": "Planets situated in Kendra houses (1st, 4th, 7th, 10th) provide foundational chart strength.",
        },
        "RULE_YOGA_BUDHA_ADITYA": {
            "ta": "சூரியனும் புதனும் இணைந்து புத-ஆதித்ய யோகத்தை அமைத்து அறிவு மற்றும் கல்வி மேன்மையை தருகிறது.",
            "en": "Sun and Mercury conjunction forms Budha-Aditya Yoga, bestowing intellect and scholarly excellence.",
        },
        "RULE_RAJA_YOGA_KENDRA_KONA": {
            "ta": "கேந்திர மற்றும் கோண அதிபதிகள் இணைந்து ராஜ யோகத்தை உருவாக்குகின்றனர்.",
            "en": "Kendra and Kona lords association forms Raja Yoga, bestowing power, honor, and success.",
        },
        "RULE_DHANA_YOGA_2_11": {
            "ta": "2-ஆம் அதிபதியும் 11-ஆம் அதிபதியும் இணைந்து தன யோகத்தை தந்து செல்வ வளம் சேர்க்கின்றனர்.",
            "en": "2nd and 11th house lords association forms Dhana Yoga, conferring wealth and financial gains.",
        },
        "RULE_ARISHTA_DUSTHANA": {
            "ta": "துஸ்தான வீடுகளில் (6, 8, 12) பாப கிரகங்கள் அமைந்து சவால்களையும் தடைகளையும் காட்டுகின்றன.",
            "en": "Natural malefics residing in Dusthana houses (6th, 8th, 12th) indicate obstacles and health challenges.",
        },
        "RULE_NEECHA_BHANGA": {
            "ta": "நீசமடைந்த கிரகம் நீச பங்கம் பெற்று ராஜ யோக சுப பலனைத் தருகிறது.",
            "en": "Debilitated planet achieves Neecha Bhanga cancellation, turning weakness into strength.",
        },
        "RULE_FUNCTIONAL_DIGNITY": {
            "ta": "லக்னாதிபதியும் கோணாதிபதிகளும் சுப கிரகங்களாக செயல்படுகின்றனர்.",
            "en": "Lagna and Kona lords act as functional benefics for the chart.",
        },
    }

    def explain_rule(self, rule_id: str, lang: str = "ta") -> str:
        """
        Generates explanation string for a given rule_id in requested language ('ta' or 'en').
        """
        target_lang = "ta" if lang.lower().startswith("ta") else "en"
        rule_trans = self.TRANSLATIONS.get(rule_id, {})
        return rule_trans.get(target_lang, f"Rule {rule_id} triggered successfully.")

    def build_summary(self, triggered_rules: List[str], lang: str = "ta") -> str:
        """
        Builds overall executive summary text in requested language.
        """
        if lang.lower().startswith("ta"):
            if not triggered_rules:
                return "ஜாதகம் சமச்சீரான நிலையில் உள்ளது."
            return f"ஜாதகத்தில் {len(triggered_rules)} முக்கிய யோகங்கள் மற்றும் அமைப்புகள் கண்டறியப்பட்டுள்ளன."
        else:
            if not triggered_rules:
                return "The horoscope shows a balanced configuration."
            return f"The horoscope features {len(triggered_rules)} prominent yogas and astrological combinations."
