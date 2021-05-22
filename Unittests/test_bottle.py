import unittest
from top_shelf.top_shelf import Bottle

class BottleTests(unittest.TestCase):
    def test_name_Uigeadail_expect_Uigeadail(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.name, "Uigeadail")

    def test_name_lowercase_expect_Titlecase(self):
        bottle = Bottle("uigeadail", "Ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.name, "Uigeadail")

    def test_name_with_integer_expect_string(self):
        bottle = Bottle(10, "Ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.name, "10")

    def test_distillery_with_Ardbeg_expect_Ardbeg(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_distillery_lowercase_expect_Titlecase(self):
        bottle = Bottle("Uigeadail", "ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_distillery_with_integer_expect_minus1(self):
        bottle = Bottle("Uigeadail", 12, 55.95, "N/A")
        self.assertEqual(bottle.distillery, -1)

    def test_price_with_55point95_expect_55point95(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55.95, "N/A")
        self.assertEqual(bottle.price, "55.95")

    def test_price_with_integer_expect_two_dps_added(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55, "N/A")
        self.assertEqual(bottle.price, "55.00")

    def test_price_with_string_expect_minus1(self):
        bottle = Bottle("Uigeadail", "Ardbeg", "Expensive", "N/A")
        self.assertEqual(bottle.price, -1)

    def test_age_NA_expect_NA(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55, "N/A")
        self.assertEqual(bottle.age, "N/A")

    def test_age_not_entered_expect_NA(self):
        bottle = Bottle("Uigeadail", "Ardbeg", 55)
        self.assertEqual(bottle.age, "N/A")

    def test_age_with_10_expect_10(self):
        bottle = Bottle("Ten", "Ardbeg", 45, 10)
        self.assertEqual(bottle.age, "10")

    def test_age_with_string_expect_minus1(self):
        bottle = Bottle("Ten", "Ardbeg", 45, "ten")
        self.assertEqual(bottle.age, -1)