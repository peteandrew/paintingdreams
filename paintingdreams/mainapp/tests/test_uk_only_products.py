from decimal import Decimal

from django.test import TestCase

from mainapp.cart import Cart
from mainapp.models import (
    Product,
    ProductType,
)

class UKOnlyProductsTestCase(TestCase):

    def setUp(self):
        self.product_type = ProductType.objects.create(
            slug = 'product-type',
            title = 'Test product type',
            price = Decimal(5.50),
            stand_alone = True,
        )
        self.product = Product.objects.create(
            product_type = self.product_type,
            uk_only = True,
            stock_count = 10,
        )

    def test_uk_only_text_on_product_page(self):
        response = self.client.get('/product/product-type')
        self.assertContains(response, 'UK orders only')

    def test_uk_only_text_in_basket(self):
        response = self.client.post('/basket-add', data={
            'product_id': self.product.id,
            'quantity': 1,
        }, follow=True)
        self.assertContains(response, '<td>Test product type<br /><span class="notice-label">UK orders only</span></td>', html=True)

    def test_non_uk_destination_remove_products_prompt(self):
        session = self.client.session
        cart = Cart(session)
        cart.add(self.product, price=self.product_type.price, quantity=1)
        session.save()

        response = self.client.post('/order-start', data={
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'customer_phone': '12345',
            'billing_address1': 'Test address',
            'billing_city': 'Some City',
            'billing_state': 'A County',
            'billing_post_code': 'AB12 3DE',
            'billing_country': 'US',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'UK only products')

    def test_non_uk_destination_products_removed(self):
        session = self.client.session
        cart = Cart(session)
        cart.add(self.product, price=self.product_type.price, quantity=1)
        session.save()

        response = self.client.post('/order-start', data={
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'customer_phone': '12345',
            'billing_address1': 'Test address',
            'billing_city': 'Some City',
            'billing_state': 'A County',
            'billing_post_code': 'AB12 3DE',
            'billing_country': 'US',
            'remove_uk_only_products': 'True',
        })
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        cart = Cart(session)
        self.assertTrue(cart.is_empty)