import unittest

from trebuchet import get_calibration_value

# Tests adapted from `problem-specifications//canonical-data.json` @ v1.7.0


class AcronymTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(get_calibration_value("d12b"), 12)


if __name__ == "__main__":
    unittest.main()
