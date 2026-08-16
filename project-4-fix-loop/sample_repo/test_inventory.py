import unittest
from inventory import apply_discount, restock, days_of_stock_left


class TestInventory(unittest.TestCase):
    def test_apply_discount(self):
        self.assertEqual(apply_discount(100, 10), 90)

    def test_restock(self):
        self.assertEqual(restock(5, 3), 8)

    def test_days_of_stock_left_full_days_only(self):
        # 10 units at 3/day = 3 full days left, not 3.333...
        self.assertEqual(days_of_stock_left(10, 3), 3)

    def test_days_of_stock_left_exact(self):
        self.assertEqual(days_of_stock_left(12, 4), 3)


if __name__ == "__main__":
    unittest.main()
