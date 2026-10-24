import unittest

from zenith_greeter.text import normalize_whitespace, slugify, truncate, word_count


class TextTests(unittest.TestCase):
    def test_normalize_whitespace(self):
        self.assertEqual(normalize_whitespace("  hello\n  world  "), "hello world")

    def test_word_count(self):
        self.assertEqual(word_count(" one   two\nthree "), 3)
        self.assertEqual(word_count("   "), 0)

    def test_slugify(self):
        self.assertEqual(slugify("Crème Brûlée & Python!"), "creme-brulee-python")
        self.assertEqual(slugify("Hello, World", separator="_"), "hello_world")
        self.assertEqual(slugify("---"), "")

    def test_slugify_rejects_empty_separator(self):
        with self.assertRaises(ValueError):
            slugify("hello", "")

    def test_truncate(self):
        self.assertEqual(truncate("abcdefgh", 5), "abcd…")
        self.assertEqual(truncate("short", 10), "short")
        self.assertEqual(truncate("abcdef", 3, "..."), "...")

    def test_truncate_zero_and_invalid_length(self):
        self.assertEqual(truncate("abc", 0), "")
        with self.assertRaises(ValueError):
            truncate("abc", -1)


if __name__ == "__main__":
    unittest.main()
