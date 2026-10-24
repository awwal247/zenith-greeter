import unittest
from datetime import date, datetime, timedelta

from zenith_greeter.dates import days_between, format_datetime, time_ago


class DateTests(unittest.TestCase):
    def test_format_datetime(self):
        self.assertEqual(
            format_datetime(datetime(2026, 10, 24, 14, 30)),
            "2026-10-24 14:30:00",
        )
        self.assertEqual(format_datetime(date(2026, 1, 2), "%d/%m/%Y"), "02/01/2026")

    def test_days_between_is_absolute(self):
        self.assertEqual(days_between(date(2026, 1, 1), date(2026, 1, 6)), 5)
        self.assertEqual(days_between(date(2026, 1, 6), date(2026, 1, 1)), 5)

    def test_days_between_rejects_datetimes(self):
        with self.assertRaises(TypeError):
            days_between(datetime(2026, 1, 1), date(2026, 1, 2))

    def test_time_ago_past_and_future(self):
        now = datetime(2026, 1, 1, 12, 0, 0)
        self.assertEqual(time_ago(now - timedelta(minutes=5), now), "5 minutes ago")
        self.assertEqual(time_ago(now + timedelta(days=2), now), "in 2 days")
        self.assertEqual(time_ago(now, now), "just now")


if __name__ == "__main__":
    unittest.main()
