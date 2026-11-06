import sqlite3
import unittest

from networks import network_counts, networks


class NetworkQueriesTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute(
            "CREATE TABLE network (bssid TEXT, ssid TEXT, capabilities TEXT, type TEXT)"
        )
        self.connection.executemany(
            "INSERT INTO network VALUES (?, ?, ?, ?)",
            [
                ("02", "Home", "second", "W"),
                ("01", "Home", "first", "W"),
                ("03", "Home", None, "E"),
                ("04", "", "", "W"),
                ("05", None, "", "W"),
                ("06", "Other", "", "W"),
                ("07", "Hidden type", "", "X"),
            ],
        )

    def tearDown(self):
        self.connection.close()

    def test_counts_match_unique_ssids_by_type(self):
        self.assertEqual(network_counts(self.connection), {"E": 1, "W": 2})

    def test_detail_matches_counts_and_selects_consistent_row(self):
        self.assertEqual(
            networks(self.connection, "W"),
            [("01", "Home", "first", "W"), ("06", "Other", "", "W")],
        )
        self.assertEqual(len(networks(self.connection, "*")), 3)
        self.assertEqual(networks(self.connection, "N"), [])

    def test_rejects_unexpected_type(self):
        with self.assertRaises(ValueError):
            networks(self.connection, "W' OR 1=1 --")


if __name__ == "__main__":
    unittest.main()
