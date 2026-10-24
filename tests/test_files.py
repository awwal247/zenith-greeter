import json
import tempfile
import unittest
from pathlib import Path

from zenith_greeter.files import ensure_directory, file_size, read_json, write_json


class FileTests(unittest.TestCase):
    def test_json_round_trip_and_size(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "data.json"
            data = {"name": "Awwal", "count": 3, "unicode": "é"}
            returned = write_json(target, data)
            self.assertEqual(returned, target)
            self.assertEqual(read_json(target), data)
            self.assertGreater(file_size(target), 0)

    def test_ensure_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "a" / "b"
            self.assertEqual(ensure_directory(target), target)
            self.assertTrue(target.is_dir())

    def test_invalid_json_error_is_not_hidden(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "bad.json"
            target.write_text("{bad", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                read_json(target)


if __name__ == "__main__":
    unittest.main()
