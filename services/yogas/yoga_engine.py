from services.yogas.budha_aditya import check as check_budha_aditya

YOGA_RULES = [
    check_budha_aditya,
]


def get_yogas(chart):

    yogas = []

    for rule in YOGA_RULES:
        result = rule(chart)

        if result:
            yogas.append(result)

    return yogas