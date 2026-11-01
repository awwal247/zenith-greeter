"""Regression tests for utility edge cases and hardened behaviour."""
import unittest
from unittest.mock import patch

from zenith_greeter.cache import TTLCache
from zenith_greeter.identifiers import random_token
from zenith_greeter.retry import retry
from zenith_greeter.text import build_query_string, parse_query_string, random_password, random_string


class TextHardeningTests(unittest.TestCase):
    def test_query_parameters_are_url_encoded(self):
        query = build_query_string({"q": "python utilities", "tag": ["a&b", "c"]})
        self.assertEqual(query, "q=python+utilities&tag=a%26b&tag=c")
        self.assertEqual(parse_query_string(query), {"q": ["python utilities"], "tag": ["a&b", "c"]})

    def test_custom_query_separator(self):
        self.assertEqual(build_query_string({"a": 1, "b": 2}, separator=";"), "a=1;b=2")

    def test_random_string_validates_length_and_alphabet(self):
        self.assertEqual(random_string(0), "")
        with self.assertRaises(ValueError):
            random_string(1, alphabet="")
        with self.assertRaises(ValueError):
            random_string(-1)

    def test_password_has_two_special_characters(self):
        for _ in range(20):
            value = random_password(12)
            self.assertEqual(len(value), 12)
            self.assertGreaterEqual(sum(char in "!@#$%^&*()" for char in value), 2)

    def test_secure_token_uses_requested_length(self):
        self.assertEqual(len(random_token(40)), 40)


class CacheHardeningTests(unittest.TestCase):
    def test_delete_returns_true_for_falsey_cached_values(self):
        cache = TTLCache()
        cache.set("empty", None)
        self.assertTrue(cache.delete("empty"))
        self.assertFalse(cache.delete("empty"))

    def test_cache_evicts_oldest_entry(self):
        cache = TTLCache(maxsize=2)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_ttl_must_be_finite_and_non_negative(self):
        with self.assertRaises(ValueError):
            TTLCache(ttl=float("inf"))
        with self.assertRaises(ValueError):
            TTLCache(ttl=-1)


class RetryHardeningTests(unittest.TestCase):
    def test_retries_then_returns_result(self):
        calls = []

        @retry(max_attempts=3, delay=0)
        def flaky():
            calls.append(True)
            if len(calls) < 3:
                raise OSError("temporary")
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(len(calls), 3)

    def test_does_not_retry_unselected_exception(self):
        calls = []

        @retry(max_attempts=3, delay=0, exceptions=(OSError,))
        def fail():
            calls.append(True)
            raise ValueError("not retryable")

        with self.assertRaises(ValueError):
            fail()
        self.assertEqual(len(calls), 1)

    def test_invalid_retry_options_are_rejected(self):
        with self.assertRaises(ValueError):
            retry(max_attempts=0)
        with self.assertRaises(ValueError):
            retry(delay=float("inf"))
        with self.assertRaises(TypeError):
            retry(jitter="yes")


if __name__ == "__main__":
    unittest.main()
