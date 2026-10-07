import runpy
import unittest
from pathlib import Path


plugin = runpy.run_path(str(Path(__file__).parents[1] / "bin" / "herdr-layout"))
placement = plugin["placement"]


class PlacementTest(unittest.TestCase):
    def test_exact_columns_and_one_column_shift(self):
        self.assertEqual(placement(120, 90, "center"), (90, 14, 14))
        self.assertEqual(placement(120, 90, "offset", -1), (90, 13, 15))
        self.assertEqual(placement(120, 90, "offset", 1), (90, 15, 13))

    def test_edges_and_narrow_terminal(self):
        self.assertEqual(placement(120, 90, "left"), (90, 0, 29))
        self.assertEqual(placement(120, 90, "right"), (90, 29, 0))
        self.assertEqual(placement(77, 90, "center"), (61, 7, 7))


if __name__ == "__main__":
    unittest.main()
