import os
import unittest
from unittest.mock import patch

from zenith_greeter.environment import get_env, get_env_bool, get_env_int


class EnvironmentTests(unittest.TestCase):
    def test_get_env_and_default(self):
        with patch.dict(os.environ, {"ZX_TEST_VALUE": "hello"}, clear=False):
            self.assertEqual(get_env("ZX_TEST_VALUE"), "hello")
        self.assertEqual(get_env("ZX_MISSING_VALUE", "fallback"), "fallback")

    def test_boolean_values(self):
        for value in ("1", "true", "YES", " on "):
            with patch.dict(os.environ, {"ZX_TEST_BOOL": value}, clear=False):
                self.assertTrue(get_env_bool("ZX_TEST_BOOL"))
        for value in ("0", "false", "NO", "off"):
            with patch.dict(os.environ, {"ZX_TEST_BOOL": value}, clear=False):
                self.assertFalse(get_env_bool("ZX_TEST_BOOL"))

    def test_boolean_default_and_invalid_value(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("ZX_MISSING_BOOL", None)
            self.assertFalse(get_env_bool("ZX_MISSING_BOOL"))
            self.assertTrue(get_env_bool("ZX_MISSING_BOOL", default=True))
        with patch.dict(os.environ, {"ZX_TEST_BOOL": "sometimes"}, clear=False):
            with self.assertRaises(ValueError):
                get_env_bool("ZX_TEST_BOOL")

    def test_integer_values(self):
        with patch.dict(os.environ, {"ZX_TEST_INT": " 42 "}, clear=False):
            self.assertEqual(get_env_int("ZX_TEST_INT"), 42)
        self.assertEqual(get_env_int("ZX_MISSING_INT", 7), 7)
        with patch.dict(os.environ, {"ZX_TEST_INT": "four"}, clear=False):
            with self.assertRaises(ValueError):
                get_env_int("ZX_TEST_INT")


if __name__ == "__main__":
    unittest.main()
