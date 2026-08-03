"""
Planet Strength Score Engine
Version 1
"""


def build_scores(strengths):

    scores = {}

    for item in strengths:

        planet = item["planet"]

        if planet not in scores:

            scores[planet] = {
                "planet": planet,
                "total_score": 0,
                "grade": "",
                "strengths": [],
            }

        scores[planet]["strengths"].append(item)

        scores[planet]["total_score"] += item["score"]

    # Grade Calculation

    for data in scores.values():

        score = data["total_score"]

        if score >= 120:
            grade = "A+"

        elif score >= 100:
            grade = "A"

        elif score >= 80:
            grade = "B+"

        elif score >= 60:
            grade = "B"

        elif score >= 40:
            grade = "C"

        else:
            grade = "D"

        data["grade"] = grade

    return list(scores.values())