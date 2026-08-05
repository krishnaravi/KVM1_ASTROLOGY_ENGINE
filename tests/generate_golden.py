"""
Regenerate the golden API snapshot.

Run this ONLY after a deliberate, approved change to chart output or to the
API contract -- never to make a failing test pass. Commit the regenerated
golden file in the same commit as the behaviour change, so the diff shows
exactly what moved.

    python tests/generate_golden.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from snapshot import GOLDEN_PATH, build_snapshot  # noqa: E402


def main():
    os.makedirs(os.path.dirname(GOLDEN_PATH), exist_ok=True)

    snapshot = build_snapshot()

    with open(GOLDEN_PATH, "w", encoding="utf-8") as handle:
        json.dump(
            snapshot,
            handle,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")

    print(
        f"wrote {GOLDEN_PATH} "
        f"({len(snapshot['responses'])} response groups)"
    )


if __name__ == "__main__":
    main()
