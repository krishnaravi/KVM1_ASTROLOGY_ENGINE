"""
Raja Yoga

Rule v1.0

A Raja Yoga is formed when
a Kendra lord and a Trikona lord
occupy the same house.
"""

from services.yogas.base import make_yoga

KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}


def check(chart):

    yogas = []

    positions = chart["house_lord_positions"]

    for k in positions:

        if k["house"] not in KENDRA:
            continue

        for t in positions:

            if t["house"] not in TRIKONA:
                continue

            # Avoid comparing same record
            if k["house"] == t["house"]:
                continue

            # Same occupied house
            if k["lord_house"] != t["lord_house"]:
                continue

            yogas.append(

                make_yoga(

                    name="Raja Yoga",

                    score=90,

                    reason=(
                        f'{k["lord"]} '
                        f'(Lord of House {k["house"]}) '
                        f'and '
                        f'{t["lord"]} '
                        f'(Lord of House {t["house"]}) '
                        f'are together in House '
                        f'{k["lord_house"]}'
                    ),

                )

            )

    return yogas