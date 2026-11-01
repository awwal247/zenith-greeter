import unittest

from zenith_greeter.numbers import clamp, in_range
from zenith_greeter.dictionaries import deep_get, deep_set
from zenith_greeter.lists import chunk, unique
from zenith_greeter.json_tools import pretty, minify
from zenith_greeter.identifiers import random_token
from zenith_greeter.pagination import paginate

class UtilityTests(unittest.TestCase):
    def test_numeric_bounds_use_the_supplied_bounds(self):
        self.assertEqual(clamp(12, 0, 10), 10)
        self.assertTrue(in_range(5, 1, 10))
        self.assertFalse(in_range(11, 1, 10))

    def test_nested_dictionary_helpers(self):
        data = {"user": {"name": "Ada"}}
        self.assertEqual(deep_get(data, "user.name"), "Ada")
        self.assertEqual(deep_get(data, "user.age", 0), 0)
        deep_set(data, "user.active", True)
        self.assertTrue(data["user"]["active"])

    def test_chunk_and_unique(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(unique([1, 1, 2, 2, 3]), [1, 2, 3])

    def test_json_formatting(self):
        self.assertEqual(minify(pretty('{"a": 1}')), '{"a":1}')

    def test_secure_token_length(self):
        self.assertEqual(len(random_token(24)), 24)

    def test_pagination_metadata(self):
        page = paginate(list(range(25)), page=2, per_page=10)
        self.assertEqual(page.items, list(range(10, 20)))
        self.assertTrue(page.has_next)
        self.assertTrue(page.has_previous)

if __name__ == "__main__":
    unittest.main()
