"""
Vedic Basic Planetary Strength Engine.
Evaluates planetary dignities (exaltation, debilitation, own sign, moolatrikona, friend, neutral, enemy sign, combustion, retrograde).
"""

from typing import List, Dict, Any
from domain.chart import ChartPlanet
from services.config.dignities import (
    EXALTATION_SIGNS,
    DEBILITATION_SIGNS,
    OWN_SIGNS,
    MOOLATRIKONA,
    FRIEND_SIGNS,
    ENEMY_SIGNS,
    NEUTRAL_SIGNS,
    COMBUSTION_LIMITS,
)


class VedicStrengthEngine:
    """
    Sub-engine responsible for Parashari dignity evaluation and strength score calculations.
    """

    def _check_dignity(self, planet: ChartPlanet) -> Dict[str, Any]:
        p = planet.name
        sign = planet.sign
        deg = planet.degree_in_sign

        # 1. Exaltation
        if p in EXALTATION_SIGNS and EXALTATION_SIGNS[p] == sign:
            return {"planet": p, "strength": "Exaltation", "score": 100, "reason": f"{p} is exalted in {sign}"}

        # 2. Debilitation
        if p in DEBILITATION_SIGNS and DEBILITATION_SIGNS[p] == sign:
            return {"planet": p, "strength": "Debilitation", "score": -100, "reason": f"{p} is debilitated in {sign}"}

        # 3. Moolatrikona
        if p in MOOLATRIKONA:
            m_sign, s_deg, e_deg = MOOLATRIKONA[p]
            if sign == m_sign and s_deg <= deg <= e_deg:
                return {"planet": p, "strength": "Moolatrikona", "score": 80, "reason": f"{p} is in Moolatrikona in {sign}"}

        # 4. Own Sign
        if p in OWN_SIGNS and sign in OWN_SIGNS[p]:
            return {"planet": p, "strength": "Own Sign", "score": 60, "reason": f"{p} is in its own sign {sign}"}

        # 5. Friend Sign
        if p in FRIEND_SIGNS and sign in FRIEND_SIGNS[p]:
            return {"planet": p, "strength": "Friend Sign", "score": 40, "reason": f"{p} is in a friendly sign {sign}"}

        # 6. Neutral Sign
        if p in NEUTRAL_SIGNS and sign in NEUTRAL_SIGNS[p]:
            return {"planet": p, "strength": "Neutral Sign", "score": 10, "reason": f"{p} is in a neutral sign {sign}"}

        # 7. Enemy Sign
        if p in ENEMY_SIGNS and sign in ENEMY_SIGNS[p]:
            return {"planet": p, "strength": "Enemy Sign", "score": -40, "reason": f"{p} is in an enemy sign {sign}"}

        return {"planet": p, "strength": "Neutral", "score": 0, "reason": f"{p} status in {sign}"}

    def _check_combustion(self, sun: ChartPlanet, planet: ChartPlanet) -> Dict[str, Any] | None:
        p = planet.name
        if p in ("Sun", "Rahu", "Ketu"):
            return None

        if p in COMBUSTION_LIMITS:
            limit = COMBUSTION_LIMITS[p]
            diff = abs(sun.longitude - planet.longitude)
            if diff > 180:
                diff = 360 - diff
            if diff <= limit:
                return {"planet": p, "strength": "Combustion", "score": -50, "reason": f"{p} is combust with Sun (diff: {diff:.2f}°)"}
        return None

    def calculate_strengths_and_scores(self, chart_planets: List[ChartPlanet]) -> Dict[str, Any]:
        """
        Evaluates dignity, combustion, retrograde rules, and builds planet scores.
        """
        strengths: List[Dict[str, Any]] = []
        sun_planet = next((p for p in chart_planets if p.name == "Sun"), None)

        for p in chart_planets:
            # 1. Primary Dignity
            dignity_rule = self._check_dignity(p)
            strengths.append(dignity_rule)

            # 2. Retrograde Rule
            if p.retrograde and p.name not in ("Rahu", "Ketu"):
                strengths.append({
                    "planet": p.name,
                    "strength": "Retrograde",
                    "score": 30,
                    "reason": f"{p.name} is in retrograde motion"
                })

            # 3. Combustion Rule
            if sun_planet and p.name != "Sun":
                comb_rule = self._check_combustion(sun_planet, p)
                if comb_rule:
                    strengths.append(comb_rule)

        # Build net scores per planet
        scores: Dict[str, int] = {}
        for p in chart_planets:
            p_rules = [s for s in strengths if s["planet"] == p.name]
            pos_score = sum(s["score"] for s in p_rules if s["score"] > 0)
            neg_score = sum(s["score"] for s in p_rules if s["score"] < 0)
            net = max(0, pos_score + neg_score)
            scores[p.name] = net

        return {
            "strengths": strengths,
            "scores": scores,
        }
