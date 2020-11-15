from django.test import TestCase

from mainapp import postage_prices
from mainapp.models import PostagePrice


class PostagePriceTestCase(TestCase):

    def setUp(self):
        PostagePrice.objects.create(
            destination='GB',
            min_weight=0,
            max_weight=500,
            price=2.5)

        PostagePrice.objects.create(
            destination='GB',
            min_weight=501,
            max_weight=1000,
            price=4)

        PostagePrice.objects.create(
            destination='GB',
            min_weight=1001,
            max_weight=3000,
            price=10)


    def test_get_postage_price_light(self):
        self.assertEqual(postage_prices.calculate('GB', 200), 2.5)


    def test_get_postage_price_medium(self):
        self.assertEqual(postage_prices.calculate('GB', 501), 4)


    def test_get_postage_price_large(self):
        self.assertEqual(postage_prices.calculate('GB', 3000), 10)


    def test_get_postage_price_greater_than_large(self):
        self.assertEqual(postage_prices.calculate('GB', 3001), 0)

    def test_get_postage_price_large_no_max_weight(self):
        PostagePrice.objects.create(
            destination='GB',
            min_weight=3001,
            price=20)
        self.assertEqual(postage_prices.calculate('GB', 3001), 20)
