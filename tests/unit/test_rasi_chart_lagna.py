import unittest

from routers.chart import rasi_chart
from routers.lagna import lagna


class TestRasiChartLagna(unittest.TestCase):

    def test_rasi_chart_exposes_house_one_lagna(self):
        chart = rasi_chart(
            "1990-05-15",
            "10:30",
            13.0827,
            80.2707,
            5.5,
        )

        self.assertIn("lagna", chart)
        self.assertEqual(chart["lagna"]["longitude"], chart["houses"][0]["longitude"])
        self.assertEqual(chart["lagna"]["sign"], chart["houses"][0]["sign"])
        self.assertEqual(chart["lagna"]["degree"], chart["houses"][0]["degree_in_sign"])

    def test_lagna_endpoint_matches_rasi_chart(self):
        chart = rasi_chart(
            "1990-05-15",
            "10:30",
            13.0827,
            80.2707,
            5.5,
        )
        endpoint_lagna = lagna(
            "1990-05-15",
            "10:30",
            13.0827,
            80.2707,
            5.5,
        )["lagna"]

        self.assertEqual(chart["lagna"]["longitude"], endpoint_lagna["longitude"])
        self.assertEqual(chart["lagna"]["sign"], endpoint_lagna["sign"])
        self.assertEqual(chart["lagna"]["degree"], endpoint_lagna["degree_in_sign"])


if __name__ == "__main__":
    unittest.main()