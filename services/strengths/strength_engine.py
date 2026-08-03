"""
Planet Strength Engine

Collects all strength rules and returns
a unified list of planet strengths.
"""

from services.strengths.exaltation import check as check_exaltation
from services.strengths.debilitation import check as check_debilitation
from services.strengths.own_sign import check as check_own_sign
from services.strengths.moolatrikona import check as check_moolatrikona
from services.strengths.friend_sign import check as check_friend_sign
from services.strengths.neutral_sign import check as check_neutral_sign
from services.strengths.enemy_sign import check as check_enemy_sign
from services.strengths.combustion import check as check_combustion
from services.strengths.retrograde import check as check_retrograde


# -------------------------------------------------------
# Dignity Rules
# (Only ONE dignity should survive for each planet)
# -------------------------------------------------------

DIGNITY_RULES = [
    check_exaltation,
    check_moolatrikona,
    check_own_sign,
    check_friend_sign,
    check_neutral_sign,
    check_enemy_sign,
    check_debilitation,
]

# -------------------------------------------------------
# Independent Rules
# (Can exist together)
# -------------------------------------------------------

OTHER_RULES = [
    check_combustion,
    check_retrograde,
]


def get_strengths(chart):

    strengths = []

    # -----------------------------------
    # Dignity
    # -----------------------------------

    dignity_found = set()

    for rule in DIGNITY_RULES:

        result = rule(chart)

        if not result:
            continue

        if not isinstance(result, list):
            result = [result]

        for item in result:

            planet = item["planet"]

            if planet in dignity_found:
                continue

            strengths.append(item)

            dignity_found.add(planet)

    # -----------------------------------
    # Independent Strengths
    # -----------------------------------

    for rule in OTHER_RULES:

        result = rule(chart)

        if not result:
            continue

        if isinstance(result, list):
            strengths.extend(result)
        else:
            strengths.append(result)

    return strengths