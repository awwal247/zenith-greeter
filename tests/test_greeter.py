"""Tests for the public Greeter API."""

import unittest

from zenith_greeter import Greeter


class GreeterTests(unittest.TestCase):
    def test_greets_named_person(self):
        self.assertEqual(
            Greeter("Awwal").greet(),
            "Hello, Awwal! Welcome to Python packages.",
        )

    def test_default_name(self):
        self.assertEqual(
            Greeter().greet(),
            "Hello, there! Welcome to Python packages.",
        )

    def test_blank_name_uses_default(self):
        self.assertEqual(
            Greeter("   ").greet(),
            "Hello, there! Welcome to Python packages.",
        )

    def test_trims_name_and_greeting(self):
        self.assertEqual(
            Greeter("  Ada  ", greeting="  Hi  ").greet(),
            "Hi, Ada! Welcome to Python packages.",
        )

    def test_custom_greeting_and_welcome_message(self):
        self.assertEqual(
            Greeter("Ada", "Welcome", "Glad you are here.").greet(),
            "Welcome, Ada! Glad you are here.",
        )

    def test_empty_welcome_message_is_omitted(self):
        self.assertEqual(Greeter("Ada", welcome_message="  ").greet(), "Hello, Ada!")

    def test_non_string_name_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "name must be a string"):
            Greeter(123)

    def test_non_string_greeting_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "greeting must be a string"):
            Greeter(greeting=123)

    def test_empty_greeting_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "greeting cannot be empty"):
            Greeter(greeting="   ")

    def test_non_string_welcome_message_raises_type_error(self):
        with self.assertRaisesRegex(TypeError, "welcome_message must be a string"):
            Greeter(welcome_message=None)


if __name__ == "__main__":
    unittest.main()
