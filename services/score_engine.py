"""
Planet Score Engine

Builds the final numerical score for each planet.

Rules
-----

Positive strengths:
    Highest dignity score only.

Negative strengths:
    Applied as penalties.
"""


def build_scores(strengths):

    scores = {}

    positive = {}

    negative = {}

    for item in strengths:

        planet = item["planet"]

        strength = item["strength"]

        score = item["score"]

        # -----------------------------
        # Negative strengths
        # -----------------------------

        if strength in (
            "Combust",
            "Debilitated",
        ):

            negative.setdefault(
                planet,
                0,
            )

            negative[planet] += score

            continue

        # -----------------------------
        # Positive strengths
        # -----------------------------

        if (
            planet not in positive
            or score > positive[planet]
        ):

            positive[planet] = score

    # -----------------------------
    # Final score
    # -----------------------------

    all_planets = set(
        positive.keys()
    ) | set(
        negative.keys()
    )

    for planet in all_planets:

        p = positive.get(
            planet,
            0,
        )

        n = negative.get(
            planet,
            0,
        )

        scores[planet] = max(
            p - n,
            0,
        )

    return scores