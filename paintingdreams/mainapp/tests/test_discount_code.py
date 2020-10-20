import uuid
from datetime import date
from decimal import Decimal

from django.test import TestCase

from mainapp.cart import Cart
from mainapp.models import (
    DiscountCode,
    DiscountCodeProduct,
    Order,
    OrderAddress,
    Product,
    ProductType,
)


class DiscountCodeTestCase(TestCase):
    def setUp(self):
        product_type_1 = ProductType.objects.create(
            slug = 'product-type1',
            title = 'Test product type 1',
            stand_alone = True,
            price = Decimal(10),
            shipping_weight = 100,
        )
        product_type_2 = ProductType.objects.create(
            slug = 'product-type2',
            title = 'Test product type 2',
            stand_alone = True,
            price = Decimal(10),
            shipping_weight = 100,
        )

        self.product_1 = Product.objects.create(
            product_type = product_type_1,
            stock_count = 1,
        )
        self.product_2 = Product.objects.create(
            product_type = product_type_2,
            stock_count = 1,
        )

        self.discount_code = DiscountCode.objects.create(
            code = 'test1234',
        )

        DiscountCodeProduct.objects.create(
            discount_code = self.discount_code,
            product = self.product_1,
            discounted_price = Decimal(5.5),
        )

        session = self.client.session
        cart = Cart(session)
        cart.add(self.product_1, price=self.product_1.product_type.price_final, quantity=1)
        cart.add(self.product_2, price=self.product_2.product_type.price_final, quantity=1)
        session.save()

    def test_apply_discount_code_non_existent_code(self):
        response = self.client.post('/apply-discount', {
            'code': 'invalidcode',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/basket')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid discount code entered')
    
    def test_apply_discount_code_expired_code(self):
        self.discount_code.valid_until = date(year=2020, month=1, day=1)
        self.discount_code.save()
    
        response = self.client.post('/apply-discount', {
            'code': 'test1234',
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/basket')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid discount code entered')

    def _test_cart_discounted_price(self):
        cart = Cart(self.client.session)
        for item in cart.items:
            if item.product.pk == self.product_1.pk:
                self.assertEqual(item.price, Decimal(5.5))
                self.assertTrue(item.discounted)
            if item.product.pk == self.product_2.pk:
                self.assertEqual(item.price, Decimal(10))
                self.assertFalse(item.discounted)

    def test_apply_discount_code_exiting_product_price_updated(self):
        response = self.client.post('/apply-discount', {
            'code': 'test1234',
        })
        self.assertEqual(response.status_code, 302)

        self.assertIn('discount_code', self.client.session)
        self.assertEqual(self.client.session['discount_code'], 'test1234')
        self._test_cart_discounted_price()

    def test_discount_code_applied_new_product_has_price_updated(self):
        session = self.client.session
        cart = Cart(session)
        cart.clear()
        cart.add(self.product_2, price=self.product_2.product_type.price_final, quantity=1)
        session['discount_code'] = 'test1234'
        session.save()

        response = self.client.post('/basket-add', {
            'product_id': self.product_1.pk,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, 302)

        self._test_cart_discounted_price()
    
    def test_discount_code_unset_when_order_complete(self):
        customer_address = OrderAddress.objects.create(
            address1 = 'Test address 1',
            post_code = 'TESTPSTCODE',
            country = 'GB'
        )
        order = Order.objects.create(
            unique_id = uuid.uuid4(),
            billing_address = customer_address,
            state = 'paid'
        )
        session = self.client.session
        session['order_id'] = str(order.unique_id)
        session['discount_code'] = 'test1234'
        session.save()

        cart = Cart(session)
        self.assertEqual(len(cart.items), 2)

        response = self.client.get('/order-complete')
        self.assertEqual(response.status_code, 200)

        cart = Cart(self.client.session)
        self.assertEqual(len(cart.items), 0)

        self.assertNotIn('discount_code', self.client.session)
    
    def test_discount_code_unset_when_basket_emptied(self):
        session = self.client.session
        session['discount_code'] = 'test1234'
        session.save()
        cart = Cart(session)
        self.assertEqual(len(cart.items), 2)

        self.client.post('/basket-change-quantity', {
            'product_id': self.product_1.pk,
            'quantity': 0,
        })
        cart = Cart(self.client.session)
        self.assertEqual(len(cart.items), 1)
        self.assertIn('discount_code', self.client.session)

        self.client.post('/basket-change-quantity', {
            'product_id': self.product_2.pk,
            'quantity': 0,
        })
        cart = Cart(self.client.session)
        self.assertEqual(len(cart.items), 0)
        self.assertNotIn('discount_code', self.client.session)
