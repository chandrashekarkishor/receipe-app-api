"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """sample"""

    def test_add_two_nums(self):
        res = calc.addition(2, 3)
        self.assertEqual(res, 5)

    def test_sub_two_nums(self):
        res = calc.subtract(5, 3)
        self.assertEqual(res, 2)
