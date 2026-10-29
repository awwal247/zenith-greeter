import unittest

from zenith_greeter.numbers import avg, clamp, in_range, is_even, is_odd, median, percentage, round_to


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

    def test_avg(self):
        self.assertEqual(avg(1, 2, 3), 2.0)
        self.assertEqual(avg(5, 10), 7.5)

    def test_avg_rejects_no_args(self):
        with self.assertRaises(ValueError):
            avg()

    def test_avg_with_bad_args(self):
        with self.assertRaises(TypeError):
            avg(True)

    def test_median_odd(self):
        self.assertEqual(median(1, 3, 2, 5, 4), 3.0)

    def test_median_even(self):
        self.assertEqual(median(1, 2, 3, 4), 2.5)

    def test_median_rejects_no_args(self):
        with self.assertRaises(ValueError):
            median()

    def test_round_to(self):
        self.assertEqual(round_to(3.14159, ndigits=2), 3.14)
        self.assertEqual(round_to(42, ndigits=0), 42)
        self.assertEqual(round_to(7.876, ndigits=1), 7.9)

    def test_round_to_invalid_ndigits(self):
        with self.assertRaises(TypeError):
            round_to(1.2, ndigits="2")
        with self.assertRaises(ValueError):
            round_to(1.2, ndigits=-1)


if __name__ == "__main__":
    unittest.main()