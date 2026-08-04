"""
Vipareeta Raja Yoga

Contains

1. Harsha Yoga
2. Sarala Yoga
3. Vimala Yoga
"""

from services.yogas.base import make_yoga

DUSTHANA = {6, 8, 12}


def check_harsha(chart):

    yogas = []

    for item in chart["house_lord_positions"]:

        if item["house"] != 6:
            continue

        if item["lord_house"] in DUSTHANA:

            yogas.append(

                make_yoga(

                    name="Harsha Yoga",

                    score=85,

                    reason=(
                        f'{item["lord"]} '
                        f'(6th Lord) '
                        f'is placed in House '
                        f'{item["lord_house"]}'
                    ),

                )

            )

    return yogas


def check_sarala(chart):

    yogas = []

    for item in chart["house_lord_positions"]:

        if item["house"] != 8:
            continue

        if item["lord_house"] in DUSTHANA:

            yogas.append(

                make_yoga(

                    name="Sarala Yoga",

                    score=85,

                    reason=(
                        f'{item["lord"]} '
                        f'(8th Lord) '
                        f'is placed in House '
                        f'{item["lord_house"]}'
                    ),

                )

            )

    return yogas


def check_vimala(chart):

    yogas = []

    for item in chart["house_lord_positions"]:

        if item["house"] != 12:
            continue

        if item["lord_house"] in DUSTHANA:

            yogas.append(

                make_yoga(

                    name="Vimala Yoga",

                    score=85,

                    reason=(
                        f'{item["lord"]} '
                        f'(12th Lord) '
                        f'is placed in House '
                        f'{item["lord_house"]}'
                    ),

                )

            )

    return yogas


def check(chart):

    yogas = []

    yogas.extend(check_harsha(chart))

    yogas.extend(check_sarala(chart))

    yogas.extend(check_vimala(chart))

    return yogas