import unittest

from zenith_greeter.text import (
    build_query_string,
    md5,
    normalize_whitespace,
    parse_query_string,
    random_password,
    random_string,
    sha256,
    slugify,
    truncate,
    word_count,
)


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

    def test_random_string(self):
        s = random_string(10)
        self.assertEqual(len(s), 10)
        self.assertTrue(all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" for c in s))

    def test_random_string_custom_alphabet(self):
        s = random_string(5, alphabet="abc")
        self.assertEqual(len(s), 5)
        self.assertTrue(all(c in "abc" for c in s))

    def test_random_password(self):
        p = random_password(12)
        self.assertEqual(len(p), 12)
        # Check it has at least some special chars (statistically likely)
        specials = "!@#$%^&*()"
        has_special = any(c in specials for c in p)
        self.assertTrue(has_special)

    def test_random_password_min_length(self):
        with self.assertRaises(ValueError):
            random_password(3)

    def test_md5(self):
        self.assertEqual(
            md5("hello"),
            "5d41402abc4b2a76b9719d911017c592",
        )
        self.assertEqual(len(md5("test")), 32)

    def test_sha256(self):
        self.assertEqual(
            sha256("hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )
        self.assertEqual(len(sha256("test")), 64)

    def test_build_query_string(self):
        self.assertEqual(build_query_string({"page": 2, "q": "hello"}), "page=2&q=hello")
        self.assertEqual(build_query_string({}), "")
        self.assertEqual(build_query_string({"a": 1, "b": 2}, separator=";"), "a=1;b=2")

    def test_parse_query_string(self):
        result = parse_query_string("?page=2&q=hello")
        self.assertEqual(result["page"], ["2"])
        self.assertEqual(result["q"], ["hello"])
        # Multiple values
        result = parse_query_string("?tag=python&tag=util")
        self.assertEqual(result["tag"], ["python", "util"])


if __name__ == "__main__":
    unittest.main()