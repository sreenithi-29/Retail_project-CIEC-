# tests/test_billing.py

import unittest
from billing import calculate_bill

class TestBilling(unittest.TestCase):
    def test_bill_with_discount_and_tax(self):
        cart_items = [
            {"product": {"id": 1, "name": "TV", "price": 25000, "category": "electronics"}, "quantity": 1},
            {"product": {"id": 2, "name": "Rice", "price": 50, "category": "groceries"}, "quantity": 2}
        ]
        bill = calculate_bill(cart_items)
        self.assertAlmostEqual(bill["subtotal"], 25100)
        self.assertAlmostEqual(bill["discount"], 2510)
        self.assertAlmostEqual(bill["taxes"], 4500.0)
        self.assertAlmostEqual(bill["total"], 25100 - 2510 + 4500)

if __name__ == "__main__":
    unittest.main()
