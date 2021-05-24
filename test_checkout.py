import unittest
from checkout import _group_offer_price, _checkout_item, checkout, Checkout


class TestCheckoutFunctions(unittest.TestCase):
    def test_group_offer_price(self):
        # Expected 1 * 25 = 25
        self.assertEqual(_group_offer_price(group_size=3, group_price=25 * 2, item_count=1, item_price=25), 25)
        # Expected 100
        self.assertEqual(_group_offer_price(group_size=3, group_price=100, item_count=3, item_price=40), 100)
        # Expected 6 + 2 * 2.5 = 11
        self.assertEqual(_group_offer_price(group_size=3, group_price=6, item_count=5, item_price=2.5), 11)

    def test_checkout_item(self):
        # Expected three for two offer, 25 * 2 + 25 * 2 = 100
        self.assertEqual(_checkout_item("A", 25, 5), 100)
        # Expected three for £100 offer, 100 * 2 + 52.5 = 100
        self.assertEqual(_checkout_item("B", 52.5, 7), 252.5)
        # Expected no offer, 33.5 * 5 = 167.5
        self.assertEqual(_checkout_item("P", 33.5, 5), 167.5)

    def test_checkout(self):
        # Expected A x1 -> 25, B x3 -> 100, P x1 -> 30, total: 155
        self.assertEqual(checkout(["B", "A", "B", "P", "B"], {"A": 25, "B": 40, "P": 30}), 155)
        # Expected A x3 -> 50, B x3 -> 100, P x2 -> 60, total: 210
        self.assertEqual(checkout(["B", "A", "B", "A", "A", "P", "P", "B"], {"A": 25, "B": 40, "P": 30}), 210)
        # Expected A x4 -> 75, B x4 -> 140, P x2 -> 60, total: 275
        self.assertEqual(checkout(["B", "A", "B", "A", "A", "B", "A", "P", "P", "B"], {"A": 25, "B": 40, "P": 30}), 275)

    def test_checkout_price_not_found(self):
        with self.assertRaises(ValueError):
            self.assertEqual(checkout(["B", "A", "B", "P", "B", "Z"], {"A": 25, "B": 40, "P": 30}), 155)


class TestCheckoutClass(unittest.TestCase):
    def setUp(self):
        self.pos = Checkout(prices={"A": 25, "B": 40, "P": 30})
        
    def test_scan(self):
        self.pos.scan("A")
        self.assertListEqual(self.pos.items, ["A"])
        self.pos.scan("B")
        self.assertListEqual(self.pos.items, ["A", "B"])
        self.pos.scan("P")
        self.assertListEqual(self.pos.items, ["A", "B", "P"])
        self.pos.scan("A")
        self.assertListEqual(self.pos.items, ["A", "B", "P", "A"])
        self.pos.scan("A")
        self.assertListEqual(self.pos.items, ["A", "B", "P", "A", "A"])

    def test_total(self):
        self.assertEqual(self.pos.total(), 0)
        for x in ["A", "B", "P", "A", "A"]:
            self.pos.scan(x)
        self.assertEqual(self.pos.total(), 120)
        for x in ["B", "B", "P"]:
            self.pos.scan(x)
        self.assertEqual(self.pos.total(), 210)

    def test_reset(self):
        for x in ["A", "B", "P", "A", "A"]:
            self.pos.scan(x)
        self.assertListEqual(self.pos.items, ["A", "B", "P", "A", "A"])
        self.pos.reset()
        self.assertListEqual(self.pos.items, [])

    def test_update_price(self):
        self.assertDictEqual(self.pos.prices, {"A": 25, "B": 40, "P": 30})
        self.pos.update_price("A", 30)
        self.assertDictEqual(self.pos.prices, {"A": 30, "B": 40, "P": 30})

    def test_set_prices(self):
        self.assertDictEqual(self.pos.prices, {"A": 25, "B": 40, "P": 30})
        self.pos.set_prices({"A": 1, "B": 2, "P": 3})
        self.assertDictEqual(self.pos.prices, {"A": 1, "B": 2, "P": 3})



if __name__ == "__main__":
    unittest.main()
