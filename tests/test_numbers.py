import unittest

from zenith_greeter.numbers import clamp, in_range, is_even, is_odd, percentage


class NumberTests(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(12, 0, 10), 10)
        self.assertEqual(clamp(-2, 0, 10), 0)
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_rejects_reversed_bounds(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)

    def test_percentage(self):
        self.assertEqual(percentage(1, 4), 25.0)
        self.assertEqual(percentage(1, 3, 1), 33.3)

    def test_percentage_zero_and_bad_precision(self):
        with self.assertRaises(ValueError):
            percentage(1, 0)
        with self.assertRaises(ValueError):
            percentage(1, 2, -1)

    def test_range_and_parity(self):
        self.assertTrue(in_range(3, 1, 3))
        self.assertFalse(in_range(4, 1, 3))
        self.assertTrue(is_even(4))
        self.assertTrue(is_odd(-3))

    def test_boolean_is_not_number_or_integer(self):
        with self.assertRaises(TypeError):
            clamp(True, 0, 2)
        with self.assertRaises(TypeError):
            is_even(True)


if __name__ == "__main__":
    unittest.main()
