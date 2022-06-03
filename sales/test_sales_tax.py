import re
import unittest
from .sales_tax import SalesTax


class SalesTaxTest(unittest.TestCase):
    data = [
        ('1 book at 12.49', '1 music CD at 14.99', '1 chocolate bar at 0.85'),
        ('1 imported box of chocolates at 10.00', '1 imported bottle of perfume at 47.50'),
        ('1 imported bottle of perfume at 27.99', '1 bottle of perfume at 18.99', '1 packet of headache pills at 9.75',
         '1 box of imported chocolates at 11.25')
    ]

    bad_data = [
        ('book at 12.49', '1 music CD at', '1 chocolate bar at 0', '1qw2 book at 12.49'),
        ('1 imported box of chocolates at 10', '1 imported bottle of perfume at 47!50',
         '1.01 imported bottle of perfume at 27.99'),
        ('1 bottle of perfume at27.99', '1 imported bottle of perfume 27.99', '1 bottle of perfumeat 27.99',
         '1 bottle of perfuatme 27.99')
    ]
    product_bad_price_values = [
        ('1 book at 1q2.49', '1 chocolate bar at 085'),
        ('1.2 imported bottle of perfume at 27.99', 'a1 bottle of perfume at 18.99', '0 packet of headache pills at 9.75')
    ]
    reg_ex = r'^\d+\s([A-Za-z]+\s?)+\sat\s[0-9]{1,6}[.,]\d{1,2}'

    def setUp(self) -> None:
        self.sales_tax = SalesTax()

    def test_reg_ex(self):
        for rows in self.data:
            for row in rows:
                self.assertIsNotNone(re.fullmatch(self.reg_ex, row))

    def test_reg_ex_bad_data(self):
        for rows in self.bad_data:
            for row in rows:
                self.assertIsNone(re.fullmatch(self.reg_ex, row))

    def test_parse_row_value_error(self):
        for rows in self.product_bad_price_values:
            for row in rows:
                self.assertRaises(ValueError, self.sales_tax.parse_row, row)

    def test_parse_row(self):
        for rows in self.data:
            for row in rows:
                product = self.sales_tax.parse_row(row)
                self.assertIsInstance(product, dict)
                self.assertIsInstance(product["tax"], int)
                self.assertIsInstance(product["total"], int)
                self.assertIsInstance(product["value"], int)
                self.assertIsInstance(product["price"], float)





