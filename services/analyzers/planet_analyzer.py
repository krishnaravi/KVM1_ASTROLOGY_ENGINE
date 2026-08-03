"""
Planet Analyzer

Analyzes each planet using the results produced by
the Strength Engine and Score Engine.

Author : KVM1_ASTROLOGY_ENGINE
Version: 1.1
"""


# ----------------------------------------------------
# Strengths that are considered DIGNITIES
# ----------------------------------------------------

DIGNITY_TYPES = {
    "Exalted",
    "Moolatrikona",
    "Own Sign",
    "Friend Sign",
    "Neutral Sign",
    "Enemy Sign",
    "Debilitated",
}


def analyze(planets, strengths, planet_scores):
    """
    Updates each ChartPlanet object.

    Sets:

    - dignity
    - strength_score
    """

    # --------------------------------------------
    # Group strengths by planet
    # --------------------------------------------

    strength_map = {}

    for item in strengths:

        planet = item["planet"]

        strength_map.setdefault(
            planet,
            [],
        )

        strength_map[planet].append(item)

    # --------------------------------------------
    # Analyze each planet
    # --------------------------------------------

    for planet in planets:

        items = strength_map.get(
            planet.name,
            [],
        )

        # ----------------------------------------
        # Default values
        # ----------------------------------------

        planet.dignity = "Normal"

        planet.strength_score = planet_scores.get(
            planet.name,
            0,
        )

        if not items:
            continue

        # ----------------------------------------
        # Only dignity rules
        # ----------------------------------------

        dignity_items = [

            item

            for item in items

            if item["strength"] in DIGNITY_TYPES

        ]

        if dignity_items:

            best = max(

                dignity_items,

                key=lambda x: x["score"],

            )

            planet.dignity = best["strength"]

    return planets