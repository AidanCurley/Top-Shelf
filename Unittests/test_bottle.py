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

    def test_distillery_empty_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "", "N/A", "55.95")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Name")

    def test_distillery_Ardbeg_expect_Ardbeg(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_distillery_lowercase_expect_Titlecase(self):
        bottle = Bottle("ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.distillery, "Ardbeg")

    def test_distillery_empty_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("", "Uigeadail", "N/A", "55.95")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Distillery")

    def test_distillery_including_numbers_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg10", "Uigeadail", "N/A", "55.95")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Distillery")

    def test_price_with_55point95_expect_55point95(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.95)
        self.assertEqual(bottle.price, 55.95)

    def test_price_with_integer_expect_two_dps_added(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55)
        self.assertEqual(bottle.price, 55.00)

    def test_price_with_three_dps_expect_two_dps_added(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55.555)
        self.assertEqual(bottle.price, 55.55)

    def test_price_with_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "Uigeadail", "N/A", "Expensive")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Price")

    def test_price_with_empty_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "Uigeadail", "N/A", "")
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Price")

    def test_age_NA_expect_0(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "N/A", 55)
        self.assertEqual(bottle.age, 0)

    def test_age_15_expect_15(self):
        bottle = Bottle("Ardbeg", "Uigeadail", 15, 55)
        self.assertEqual(bottle.age, 15)

    def test_age_with_empty_string_expect_0(self):
        bottle = Bottle("Ardbeg", "Uigeadail", "", 55)
        self.assertEqual(bottle.age, 0)

    def test_age_with_string_expect_inputerror(self):
        with self.assertRaises(InputError) as cm:
            bottle = Bottle("Ardbeg", "Ten", "ten", 45)
            the_exception = cm.exception
            self.assertEqual(the_exception.title, "Age")

