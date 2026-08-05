"""
Shared snapshot builder for the golden-chart regression suite.

Calls each router handler directly and serialises the result with FastAPI's own
``jsonable_encoder`` -- byte-identical to what the HTTP layer emits -- so the
suite needs no running server and no HTTP client dependency.

The OpenAPI schema is captured alongside the responses because it *is* the API
contract: route paths, query parameters and response shapes all live there.
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

GOLDEN_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "golden",
    "api_snapshot.json",
)

# Fixtures deliberately span both hemispheres, eastern and western longitudes,
# a high-latitude chart, and times across the full day, so the Placidus, sign,
# dignity and yoga paths are all exercised.
CASES = [
    ("1990-05-15", "10:30", 13.0827, 80.2707),    # Chennai
    ("1985-11-02", "03:45", 28.6139, 77.2090),    # Delhi, pre-dawn
    ("2001-07-21", "23:15", 19.0760, 72.8777),    # Mumbai, late night
    ("1972-01-09", "06:00", 9.9312, 76.2673),     # Kochi
    ("2010-12-31", "12:00", 51.5074, -0.1278),    # London, western longitude
    ("1996-03-08", "17:40", -33.8688, 151.2093),  # Sydney, southern hemisphere
    ("1968-08-25", "08:05", 59.9139, 10.7522),    # Oslo, high latitude
]


def build_snapshot():
    """Return the full {openapi, responses} snapshot as plain JSON-able data."""

    from fastapi.encoders import jsonable_encoder

    from main import app, calculate_horoscope
    from routers.chart import rasi_chart
    from routers.health import health
    from routers.house import houses
    from routers.lagna import lagna
    from routers.planet import planets_positions

    snapshot = {
        "openapi": app.openapi(),
        "responses": {"health": jsonable_encoder(health())},
    }

    for date, time, latitude, longitude in CASES:
        key = f"{date}T{time}@{latitude},{longitude}"

        snapshot["responses"][key] = {
            "lagna": jsonable_encoder(lagna(date, time, latitude, longitude)),
            "houses": jsonable_encoder(houses(date, time, latitude, longitude)),
            "planet_positions": jsonable_encoder(
                planets_positions(date, time)
            ),
            "rasi_chart": jsonable_encoder(
                rasi_chart(date, time, latitude, longitude)
            ),
            "legacy_horoscope": jsonable_encoder(
                calculate_horoscope(date, time)
            ),
        }

    return snapshot


def find_differences(expected, actual, path="", out=None):
    """
    Recursively collect human-readable differences.

    Returns a list of strings rather than dumping two 180 KB blobs, so a
    regression names the exact key that moved.
    """

    if out is None:
        out = []

    if type(expected) is not type(actual):
        out.append(
            f"{path or '<root>'}: type {type(expected).__name__} "
            f"-> {type(actual).__name__}"
        )
        return out

    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual)):
            sub = f"{path}.{key}" if path else str(key)

            if key not in actual:
                out.append(f"{sub}: KEY REMOVED (was {expected[key]!r})")
            elif key not in expected:
                out.append(f"{sub}: KEY ADDED (now {actual[key]!r})")
            else:
                find_differences(expected[key], actual[key], sub, out)

    elif isinstance(expected, list):
        if len(expected) != len(actual):
            out.append(
                f"{path}: length {len(expected)} -> {len(actual)}"
            )

        for i, (e, a) in enumerate(zip(expected, actual)):
            find_differences(e, a, f"{path}[{i}]", out)

    elif expected != actual:
        out.append(f"{path}: {expected!r} -> {actual!r}")

    return out
