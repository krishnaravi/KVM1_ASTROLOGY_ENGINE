import unittest

from services.yogas.dhana_yoga import check


class TestDhanaYoga(unittest.TestCase):

    def chart(self, positions):
        return {"house_lord_positions": positions}

    def position(self, house, lord, lord_house):
        return {
            "house": house,
            "lord": lord,
            "lord_house": lord_house,
        }

    def test_valid_wealth_trinal_pairs(self):
        cases = ((2, 5), (2, 9), (11, 5), (11, 9))

        for wealth_house, trinal_house in cases:
            with self.subTest(wealth_house=wealth_house, trinal_house=trinal_house):
                result = check(self.chart([
                    self.position(wealth_house, "Venus", 10),
                    self.position(trinal_house, "Saturn", 10),
                ]))
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["name"], "Dhana Yoga")
                self.assertEqual(result[0]["score"], 85)

    def test_different_houses_do_not_form_yoga(self):
        result = check(self.chart([
            self.position(2, "Venus", 10),
            self.position(5, "Saturn", 11),
        ]))

        self.assertEqual(result, [])

    def test_unrelated_lord_does_not_form_yoga(self):
        result = check(self.chart([
            self.position(2, "Venus", 10),
            self.position(3, "Saturn", 10),
        ]))

        self.assertEqual(result, [])

    def test_missing_positions_do_not_form_yoga(self):
        self.assertEqual(check({}), [])

    def test_duplicate_ownership_paths_emit_one_result(self):
        result = check(self.chart([
            self.position(2, "Venus", 10),
            self.position(11, "Venus", 10),
            self.position(5, "Saturn", 10),
        ]))

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["reason"],
            "2nd lord Venus and 5th lord Saturn are together in House 10",
        )


if __name__ == "__main__":
    unittest.main()