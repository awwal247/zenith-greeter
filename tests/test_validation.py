import unittest

from zenith_greeter.validation import is_non_empty_string, is_valid_email, is_valid_url


class ValidationTests(unittest.TestCase):
    def test_non_empty_string(self):
        self.assertTrue(is_non_empty_string(" hello "))
        self.assertFalse(is_non_empty_string("   "))
        self.assertFalse(is_non_empty_string(123))

    def test_email_shape(self):
        self.assertTrue(is_valid_email("person@example.com"))
        self.assertFalse(is_valid_email("not-an-email"))
        self.assertFalse(is_valid_email("a b@example.com"))

    def test_http_urls(self):
        self.assertTrue(is_valid_url("https://example.com/path"))
        self.assertTrue(is_valid_url("http://localhost:8000"))
        self.assertFalse(is_valid_url("ftp://example.com"))
        self.assertFalse(is_valid_url("/relative/path"))


if __name__ == "__main__":
    unittest.main()
