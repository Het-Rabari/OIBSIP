import math
import unittest

try:
    from .bmi_calculator import bmi_category, calculate_bmi
except ImportError:
    from bmi_calculator import bmi_category, calculate_bmi


class BmiCalculatorTests(unittest.TestCase):
    def test_calculates_bmi_from_kilograms_and_centimeters(self):
        self.assertAlmostEqual(calculate_bmi(70, 175), 22.8571428571)

    def test_classifies_adult_bmi_boundaries(self):
        cases = [
            (18.49, "Underweight"),
            (18.5, "Normal weight"),
            (24.99, "Normal weight"),
            (25, "Overweight"),
            (29.99, "Overweight"),
            (30, "Obesity"),
        ]
        for bmi, expected in cases:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_category(bmi), expected)

    def test_rejects_zero_and_negative_measurements(self):
        for weight, height in [(0, 170), (-1, 170), (70, 0), (70, -1)]:
            with self.subTest(weight=weight, height=height):
                with self.assertRaises(ValueError):
                    calculate_bmi(weight, height)

    def test_rejects_non_finite_measurements(self):
        for weight, height in [(math.nan, 170), (70, math.inf)]:
            with self.subTest(weight=weight, height=height):
                with self.assertRaises(ValueError):
                    calculate_bmi(weight, height)

    def test_rejects_invalid_bmi_category_input(self):
        for bmi in [0, -1, math.inf, math.nan, "not a number"]:
            with self.subTest(bmi=bmi):
                with self.assertRaises(ValueError):
                    bmi_category(bmi)


if __name__ == "__main__":
    unittest.main()
