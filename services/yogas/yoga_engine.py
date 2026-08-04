"""
Yoga Engine

Runs all Yoga Rules.
"""

from services.yogas.budha_aditya import check as check_budha_aditya
from services.yogas.raja_yoga import check as check_raja_yoga
from services.yogas.dhana_yoga import check as check_dhana_yoga
from services.yogas.gaja_kesari import check as check_gaja_kesari
from services.yogas.neecha_bhanga import check as check_neecha_bhanga
from services.yogas.vipareetha import check as check_vipareetha




YOGA_RULES = [

    check_budha_aditya,

    check_raja_yoga,

    check_dhana_yoga,

    check_gaja_kesari,

    check_neecha_bhanga,

    check_vipareetha,

]


def get_yogas(chart):

    yogas = []

    for rule in YOGA_RULES:

        result = rule(chart)

        if not result:
            continue

        if isinstance(result, list):
            yogas.extend(result)
        else:
            yogas.append(result)

    return yogas