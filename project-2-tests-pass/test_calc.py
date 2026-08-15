import unittest
from calc import add, is_even, factorial


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_is_even(self):
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(3))

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)


if __name__ == "__main__":
    unittest.main()
