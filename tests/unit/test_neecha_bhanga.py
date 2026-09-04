import unittest
from types import SimpleNamespace

from services.yogas.neecha_bhanga import check


class TestNeechaBhanga(unittest.TestCase):

    def chart(self, mars_house, moon_house, mars_sign="கடகம்"):
        return {
            "planets": [
                SimpleNamespace(name="Mars", sign=mars_sign, house=mars_house),
                SimpleNamespace(name="Moon", sign="மேஷம்", house=moon_house),
            ]
        }

    def test_mars_cancellation_in_each_kendra(self):
        for moon_house in (1, 4, 7, 10):
            with self.subTest(moon_house=moon_house):
                result = check(self.chart(8, moon_house))
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["name"], "Neecha Bhanga Yoga")
                self.assertEqual(result[0]["house"], moon_house)

    def test_non_kendra_sign_lord_does_not_cancel(self):
        for moon_house in (2, 3, 5):
            with self.subTest(moon_house=moon_house):
                self.assertEqual(check(self.chart(8, moon_house)), [])

    def test_planet_not_in_debilitation_sign_does_not_match(self):
        self.assertEqual(check(self.chart(8, 1, mars_sign="சிம்மம்")), [])

    def test_missing_planet_data_does_not_match(self):
        self.assertEqual(check({}), [])
        self.assertEqual(check({"planets": [SimpleNamespace(name="Mars", sign="கடகம்")]}), [])

    def test_one_debilitated_planet_emits_one_result(self):
        result = check(self.chart(8, 1))

        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()