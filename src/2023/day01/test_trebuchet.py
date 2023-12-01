import unittest

from trebuchet import get_calibration_value, get_digit


class Test(unittest.TestCase):
    def test_1(self):
        self.assertEqual(get_calibration_value("d12b"), 12)

    def test_2(self):
        self.assertEqual(get_digit("one"), 1)


if __name__ == "__main__":
    unittest.main()
