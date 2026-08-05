"""
Golden-chart regression tests.

Pins the serialised response of every endpoint across the fixture charts, plus
the generated OpenAPI schema. Any change to chart output, response keys, route
paths or query parameters fails here.

    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snapshot import (  # noqa: E402
    CASES,
    GOLDEN_PATH,
    build_snapshot,
    find_differences,
)

MAX_REPORTED_DIFFS = 25


def _load_golden():
    with open(GOLDEN_PATH, encoding="utf-8") as handle:
        return json.load(handle)


class GoldenSnapshotTest(unittest.TestCase):
    """Compares a freshly built snapshot against the committed golden file."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(GOLDEN_PATH):
            raise unittest.SkipTest(
                f"golden file missing: {GOLDEN_PATH} "
                f"(run: python tests/generate_golden.py)"
            )

        cls.golden = _load_golden()
        cls.current = build_snapshot()

    def _assert_matches(self, expected, actual, label):
        diffs = find_differences(expected, actual)

        if not diffs:
            return

        shown = diffs[:MAX_REPORTED_DIFFS]
        hidden = len(diffs) - len(shown)

        report = "\n".join(f"  {line}" for line in shown)

        if hidden > 0:
            report += f"\n  ... and {hidden} more difference(s)"

        self.fail(
            f"{label} diverged from the golden snapshot "
            f"({len(diffs)} difference(s)):\n{report}"
        )

    # -- API contract ---------------------------------------------------

    def test_openapi_schema_unchanged(self):
        """Route paths, query params and response shapes must not move."""

        self._assert_matches(
            self.golden["openapi"],
            self.current["openapi"],
            "OpenAPI schema",
        )

    def test_no_endpoint_removed_or_added(self):
        self.assertEqual(
            sorted(self.golden["openapi"]["paths"]),
            sorted(self.current["openapi"]["paths"]),
            "the set of registered routes changed",
        )

    # -- Response payloads ----------------------------------------------

    def test_health_unchanged(self):
        self._assert_matches(
            self.golden["responses"]["health"],
            self.current["responses"]["health"],
            "/health",
        )

    def test_all_fixture_charts_covered(self):
        expected_keys = {
            f"{d}T{t}@{lat},{lon}" for d, t, lat, lon in CASES
        }

        self.assertTrue(
            expected_keys.issubset(set(self.golden["responses"])),
            "golden file predates the current fixture list; "
            "run: python tests/generate_golden.py",
        )


def _make_chart_test(case_key, endpoint):
    def test(self):
        self._assert_matches(
            self.golden["responses"][case_key][endpoint],
            self.current["responses"][case_key][endpoint],
            f"{endpoint} for {case_key}",
        )

    return test


# One test method per (chart, endpoint) pair, so a failure names the exact
# fixture and endpoint that moved instead of one opaque assertion.
for _date, _time, _lat, _lon in CASES:
    _key = f"{_date}T{_time}@{_lat},{_lon}"
    _slug = (
        _key.replace("-", "_")
        .replace(":", "")
        .replace("@", "_at_")
        .replace(",", "_")
        .replace(".", "p")
        .replace("T", "_")
    )

    for _endpoint in (
        "lagna",
        "houses",
        "planet_positions",
        "rasi_chart",
        "legacy_horoscope",
    ):
        setattr(
            GoldenSnapshotTest,
            f"test_{_endpoint}__{_slug}",
            _make_chart_test(_key, _endpoint),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
