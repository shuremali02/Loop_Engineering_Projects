import unittest
from utils import average, truncate, is_weekend


class TestUtils(unittest.TestCase):
    def test_average(self):
        self.assertEqual(average([1, 2, 3, 4]), 2.5)

    def test_truncate(self):
        self.assertEqual(truncate("hello world", 5), "hello...")

    def test_is_weekend_saturday(self):
        self.assertTrue(is_weekend(5))

    def test_is_weekend_sunday(self):
        self.assertTrue(is_weekend(6))


if __name__ == "__main__":
    unittest.main()
