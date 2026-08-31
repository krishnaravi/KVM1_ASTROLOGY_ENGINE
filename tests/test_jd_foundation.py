"""
Phase-1 foundation tests: Julian Day and sidereal-mode consolidation.

These guard the STRUCTURAL invariants introduced by the Phase-1 refactor.
They deliberately assert nothing about astrological meaning -- the golden
suite in test_golden_charts.py covers output.

    python -m unittest discover -s tests -v
"""

import ast
import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snapshot import CASES, REPO_ROOT  # noqa: E402

sys.path.insert(0, REPO_ROOT)

import swisseph as swe  # noqa: E402

from core.constants import SIDEREAL_MODE  # noqa: E402
from core.swisseph_service import get_julian_day  # noqa: E402

# The canonical module is the only place allowed to call these.
CANONICAL_MODULE = os.path.join("core", "swisseph_service.py")

FIRST_PARTY_DIRS = ("core", "domain", "models", "routers", "services")


def _iter_first_party_sources():
    """Yield (repo_relative_path, source_text) for every first-party module."""

    targets = [os.path.join(REPO_ROOT, "main.py")]

    for directory in FIRST_PARTY_DIRS:
        for root, _dirs, files in os.walk(os.path.join(REPO_ROOT, directory)):
            if "__pycache__" in root:
                continue

            for name in sorted(files):
                if name.endswith(".py"):
                    targets.append(os.path.join(root, name))

    for path in targets:
        rel = os.path.relpath(path, REPO_ROOT)

        with open(path, encoding="utf-8") as handle:
            yield rel, handle.read()


def _swe_calls(source, attr):
    """Return line numbers of every ``swe.<attr>(...)`` call in source."""

    tree = ast.parse(source)
    hits = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        func = node.func

        if (
            isinstance(func, ast.Attribute)
            and func.attr == attr
            and isinstance(func.value, ast.Name)
            and func.value.id == "swe"
        ):
            hits.append(node.lineno)

    return hits


# ---------------------------------------------------------------------
# A. get_julian_day() determinism
# ---------------------------------------------------------------------


class JulianDayDeterminismTest(unittest.TestCase):
    def test_repeated_calls_are_identical(self):
        for date, time, _lat, _lon in CASES:
            first = get_julian_day(date, time)

            for _ in range(3):
                self.assertEqual(
                    first,
                    get_julian_day(date, time),
                    f"get_julian_day is not deterministic for {date} {time}",
                )

    def test_distinct_inputs_give_distinct_results(self):
        seen = {}

        for date, time, _lat, _lon in CASES:
            jd = get_julian_day(date, time)

            self.assertNotIn(
                jd,
                seen,
                f"{date} {time} collides with {seen.get(jd)}",
            )

            seen[jd] = f"{date} {time}"

    def test_one_minute_advances_by_one_minute(self):
        base = get_julian_day("1990-05-15", "10:30")
        later = get_julian_day("1990-05-15", "10:31")

        self.assertAlmostEqual(
            (later - base) * 24 * 60,
            1.0,
            places=6,
            msg="one minute of input did not advance JD by one minute",
        )

    def test_invalid_input_still_raises_value_error(self):
        for date, time in (
            ("not-a-date", "10:30"),
            ("1990-05-15", "25:99"),
            ("1990-13-01", "10:30"),
        ):
            with self.assertRaises(ValueError):
                get_julian_day(date, time)


# ---------------------------------------------------------------------
# B. Equivalence with the exact pre-refactor arithmetic
# ---------------------------------------------------------------------


def _legacy_julian_day(date_str, time_str):
    """
    The exact arithmetic that existed, duplicated, before Phase-1.

    Reproduced verbatim so the refactor is provably value-preserving.
    """

    dt = datetime.strptime(
        f"{date_str} {time_str}",
        "%Y-%m-%d %H:%M",
    )

    return swe.julday(
        dt.year,
        dt.month,
        dt.day,
        dt.hour + dt.minute / 60.0,
    )


class JulianDayEquivalenceTest(unittest.TestCase):
    """The canonical helper must equal the old inline arithmetic exactly."""

    def test_matches_legacy_arithmetic_on_all_fixture_charts(self):
        for date, time, _lat, _lon in CASES:
            self.assertEqual(
                _legacy_julian_day(date, time),
                get_julian_day(date, time),
                f"JD changed for fixture {date} {time}",
            )

    def test_matches_legacy_arithmetic_on_edge_times(self):
        edge_cases = [
            ("1990-05-15", "00:00"),
            ("1990-05-15", "23:59"),
            ("2000-01-01", "12:00"),
            ("2000-02-29", "06:30"),   # leap day
            ("1900-01-01", "00:01"),
            ("2100-12-31", "23:58"),
        ]

        for date, time in edge_cases:
            self.assertEqual(
                _legacy_julian_day(date, time),
                get_julian_day(date, time),
                f"JD changed for edge case {date} {time}",
            )

    def test_no_timezone_offset_is_applied(self):
        """
        Phase-1 must NOT convert local time to UT.

        Two inputs five and a half hours apart must remain five and a half
        hours apart in JD -- i.e. the value tracks the wall clock verbatim.

        Tolerance is 1e-6 hours (~3.6 ms). A Julian Day is ~2.45e6, so
        double precision resolves roughly 1e-9 days; demanding more than
        that would test the float format, not the code. Any real timezone
        offset would be at least 0.5 h -- five orders of magnitude larger.
        """

        base = get_julian_day("1990-05-15", "05:00")
        later = get_julian_day("1990-05-15", "10:30")

        self.assertAlmostEqual(
            (later - base) * 24,
            5.5,
            places=6,
            msg="an unexpected timezone offset was applied",
        )


# ---------------------------------------------------------------------
# C. Sidereal mode remains Lahiri
# ---------------------------------------------------------------------


class SiderealModeTest(unittest.TestCase):
    def test_constant_is_lahiri(self):
        self.assertEqual(SIDEREAL_MODE, swe.SIDM_LAHIRI)

    def test_canonical_module_configures_from_the_constant(self):
        """The one remaining call must read SIDEREAL_MODE, not a literal."""

        path = os.path.join(REPO_ROOT, CANONICAL_MODULE)

        with open(path, encoding="utf-8") as handle:
            source = handle.read()

        self.assertIn("swe.set_sid_mode(SIDEREAL_MODE)", source)
        self.assertNotIn("swe.set_sid_mode(swe.SIDM_LAHIRI)", source)


# ---------------------------------------------------------------------
# D. Redundant / request-path configuration has been removed
# ---------------------------------------------------------------------


class ConsolidationTest(unittest.TestCase):
    def test_julday_called_only_in_canonical_module(self):
        offenders = {
            rel: lines
            for rel, source in _iter_first_party_sources()
            if (lines := _swe_calls(source, "julday"))
            and rel != CANONICAL_MODULE
        }

        self.assertEqual(
            offenders,
            {},
            f"swe.julday() must only be called in {CANONICAL_MODULE}; "
            f"found {offenders}",
        )

    def test_set_sid_mode_called_only_in_canonical_module(self):
        offenders = {
            rel: lines
            for rel, source in _iter_first_party_sources()
            if (lines := _swe_calls(source, "set_sid_mode"))
            and rel != CANONICAL_MODULE
        }

        self.assertEqual(
            offenders,
            {},
            f"swe.set_sid_mode() must only be called in {CANONICAL_MODULE}; "
            f"found {offenders}",
        )

    def test_canonical_module_configures_ayanamsa_exactly_once(self):
        path = os.path.join(REPO_ROOT, CANONICAL_MODULE)

        with open(path, encoding="utf-8") as handle:
            calls = _swe_calls(handle.read(), "set_sid_mode")

        self.assertEqual(
            len(calls),
            1,
            f"expected exactly one set_sid_mode call, found {len(calls)}",
        )

    def test_no_sidereal_reconfiguration_during_requests(self):
        """
        Behavioural proof that the request path no longer reconfigures the
        ayanamsa: serving every endpoint must trigger zero set_sid_mode calls.
        """

        from routers.chart import rasi_chart
        from routers.house import houses
        from routers.lagna import lagna
        from routers.planet import planets_positions

        calls = []
        original = swe.set_sid_mode

        def counting_set_sid_mode(*args, **kwargs):
            calls.append(args)
            return original(*args, **kwargs)

        swe.set_sid_mode = counting_set_sid_mode

        try:
            date, time, lat, lon = CASES[0]

            lagna(date, time, lat, lon)
            houses(date, time, lat, lon)
            planets_positions(date, time)
            rasi_chart(date, time, lat, lon)
        finally:
            swe.set_sid_mode = original

        self.assertEqual(
            calls,
            [],
            f"ayanamsa was reconfigured {len(calls)} time(s) during requests",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
