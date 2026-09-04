import unittest
from types import SimpleNamespace

from services.yogas.gaja_kesari import check


class TestGajaKesari(unittest.TestCase):

    def chart(self, moon_house, jupiter_house):
        return {
            "planets": [
                SimpleNamespace(name="Moon", house=moon_house),
                SimpleNamespace(name="Jupiter", house=jupiter_house),
            ]
        }

    def test_kendra_relationships_pass(self):
        for jupiter_house in (1, 4, 7, 10):
            with self.subTest(jupiter_house=jupiter_house):
                result = check(self.chart(1, jupiter_house))
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["name"], "Gaja Kesari Yoga")
                self.assertTrue(result[0]["found"])

    def test_wraparound_relationship_passes(self):
        result = check(self.chart(10, 1))

        self.assertEqual(len(result), 1)
        self.assertIn("4th from Moon", result[0]["reason"])

    def test_non_kendra_relationships_fail(self):
        for relative_house in (2, 3, 5, 6, 8, 9, 11, 12):
            with self.subTest(relative_house=relative_house):
                result = check(self.chart(1, relative_house))
                self.assertEqual(result, [])

    def test_missing_planet_fails_without_duplicate_result(self):
        self.assertEqual(check({"planets": []}), [])


if __name__ == "__main__":
    unittest.main()