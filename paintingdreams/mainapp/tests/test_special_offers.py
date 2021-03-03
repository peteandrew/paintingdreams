from decimal import Decimal

from django.test import TestCase

from mainapp.models import (
    Product,
    ProductType,
)

class SpecialOffersTestCase(TestCase):

    def setUp(self):
        self.product_type_1 = ProductType.objects.create(
            slug = 'product-type1',
            title = 'Test product type 1',
            price = Decimal(5.50),
            stand_alone = True,
        )
        self.product_type_2 = ProductType.objects.create(
            slug = 'product-type2',
            title = 'Test product type 2',
            price = Decimal(6.25),
            special_offer_price = Decimal(3.30),
            stand_alone = True,
        )
        self.product_type_3 = ProductType.objects.create(
            slug = 'product-type3',
            title = 'Test product type 3',
            price = Decimal(10),
            stand_alone = True,
        )
        self.product_1 = Product.objects.create(
            product_type = self.product_type_1,
        )
        self.product_2 = Product.objects.create(
            product_type = self.product_type_2,
        )
        self.product_3 = Product.objects.create(
            product_type = self.product_type_3,
            special_offer_price = Decimal(8.25),
        )

    def test_correct_product_special_offer_state_returned(self):
        self.assertFalse(self.product_1.special_offer)
        self.assertTrue(self.product_2.special_offer)
        self.assertTrue(self.product_3.special_offer)

    def test_correct_prices_returned(self):
        self.assertEqual(self.product_1.price, Decimal(5.50))
        self.assertEqual(self.product_1.old_price, Decimal(5.50))
        self.assertEqual(self.product_2.price, Decimal(3.30))
        self.assertEqual(self.product_2.old_price, Decimal(6.25))
        self.assertEqual(self.product_3.price, Decimal(8.25))
        self.assertEqual(self.product_3.old_price, Decimal(10))

    def test_special_offer_products_listed(self):
        # Special offers page should list product_2 and product_3
        response = self.client.get('/special-offers')
        self.assertNotContains(response, 'Test product type 1')
        self.assertContains(response, 'Test product type 2')
        self.assertContains(response, 'Test product type 3')

    def test_sold_out_special_offer_products_not_listed(self):
        self.product_2.sold_out = True
        self.product_2.save()
        # Special offers page should only list product_3
        response = self.client.get('/special-offers')
        self.assertNotContains(response, 'Test product type 1')
        self.assertNotContains(response, 'Test product type 2')
        self.assertContains(response, 'Test product type 3')

    def test_hidden_special_offer_products_not_listed(self):
        self.product_3.hidden = True
        self.product_3.save()
        # Special offers page should only list product_3
        response = self.client.get('/special-offers')
        self.assertNotContains(response, 'Test product type 1')
        self.assertContains(response, 'Test product type 2')
        self.assertNotContains(response, 'Test product type 3')

    def test_special_offer_price_on_product_details(self):
        response = self.client.get('/product/product-type2')
        self.assertContains(response, 'Original price: &pound;6.25')
        self.assertContains(response, 'Special offer price: &pound;3.30')
        response = self.client.get('/product/product-type3')
        self.assertContains(response, 'Original price: &pound;10')
        self.assertContains(response, 'Special offer price: &pound;8.25')

    def test_original_price_not_shown_when_special_offer_price_equals_old_price(self):
        self.product_3.special_offer_price = Decimal(10)
        self.product_3.save()
        response = self.client.get('/product/product-type3')
        self.assertNotContains(response, 'Original price: &pound;10')
        self.assertContains(response, 'Special offer price: &pound;10')

    def test_special_offer_price_in_basket(self):
        response = self.client.post('/basket-add', data={
            'product_id': self.product_2.id,
            'quantity': 1,
        }, follow=True)
        self.assertContains(response, '<td>Test product type 2<br /><span class="notice-label">special offer</span></td>', html=True)
        self.assertContains(response, '<td>&pound;3.30</td>', html=True)