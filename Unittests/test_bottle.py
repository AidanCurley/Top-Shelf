import unittest
from main_app.main_application import Bottle, InputError
class BottleTests(unittest.TestCase):
    def test_name_Uigeadail_expect_Uigeadail(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.name, "Uigeadail")

    def test_name_lowercase_expect_Titlecase(self):
        bottle = Bottle("Ardbeg", "uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.name, "Uigeadail")

    def test_name_with_integer_expect_string(self):
        bottle = Bottle("Ardbeg", 10, "N/A", 55.95)
        self.assertEqual(bottle.name, "10")

    def test_distillery_with_Ardbeg_expect_Ardbeg(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_distillery_lowercase_expect_Titlecase(self):
        bottle = Bottle("ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_price_with_55point95_expect_55point95(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.price, "55.95")

    def test_price_with_integer_expect_two_dps_added(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55)
        self.assertEqual(bottle.price, "55.00")

    def test_price_with_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "Uigeadail", "N/A", "Expensive")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Price")


    def test_age_NA_expect_NA(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55)
        self.assertEqual(bottle.age, "N/A")

    def test_age_with_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "Ten", "ten", 45)
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Age")
