"""
Dhana Yoga
"""

from services.yogas.base import make_yoga


WEALTH_HOUSES = (2, 11)
TRINAL_HOUSES = (5, 9)


def _ordinal(house):
    return {
        2: "2nd",
        5: "5th",
        9: "9th",
        11: "11th",
    }[house]


def check(chart):
    positions = chart.get("house_lord_positions", [])
    seen = set()
    yogas = []

    for wealth_house in WEALTH_HOUSES:
        wealth_positions = [
            position
            for position in positions
            if position.get("house") == wealth_house
        ]

        for trinal_house in TRINAL_HOUSES:
            trinal_positions = [
                position
                for position in positions
                if position.get("house") == trinal_house
            ]

            for wealth in wealth_positions:
                for trinal in trinal_positions:
                    if wealth.get("lord") == trinal.get("lord"):
                        continue

                    if wealth.get("lord_house") != trinal.get("lord_house"):
                        continue

                    pair_key = (
                        frozenset((wealth["lord"], trinal["lord"])),
                        wealth["lord_house"],
                    )
                    if pair_key in seen:
                        continue

                    seen.add(pair_key)
                    yogas.append(
                        make_yoga(
                            name="Dhana Yoga",
                            score=85,
                            reason=(
                                f"{wealth_house and _ordinal(wealth_house)} lord "
                                f"{wealth['lord']} and "
                                f"{_ordinal(trinal_house)} lord {trinal['lord']} "
                                f"are together in House {wealth['lord_house']}"
                            ),
                        )
                    )

    return yogas