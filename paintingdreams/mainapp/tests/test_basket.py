from decimal import Decimal

from django.test import TestCase

from mainapp.cart import Cart
from mainapp.models import (
    PostagePrice,
    Product,
    ProductType,
)


class BasketTotalTestCase(TestCase):
    def setUp(self):
        product_type_1 = ProductType.objects.create(
            slug = 'product-type1',
            title = 'Test product type 1',
            stand_alone = True,
            price = Decimal(10),
            shipping_weight = 100,
        )
        self.product_1 = Product.objects.create(
            product_type = product_type_1,
            stock_count = 1,
        )

        session = self.client.session
        cart = Cart(session)
        cart.add(self.product_1, price=self.product_1.product_type.price_final, quantity=1)
        session.save()

    def test_total_no_postage_price(self):
        response = self.client.get('/basket')
        self.assertEqual(response.context['postage_price'], 0)
        self.assertEqual(response.context['order_total'], Decimal(10))

    def test_total_with_postage_price(self):
        PostagePrice.objects.create(
            destination = 'GB',
            min_weight=0,
            price=Decimal(5),
        )
        response = self.client.get('/basket')
        self.assertEqual(response.context['postage_price'], Decimal(5))
        self.assertEqual(response.context['order_total'], Decimal(15))

    def test_total_with_postage_price_product_sold_out(self):
        PostagePrice.objects.create(
            destination = 'GB',
            min_weight=0,
            price=Decimal(5),
        )
        self.product_1.sold_out = True
        self.product_1.save()
        response = self.client.get('/basket')
        self.assertEqual(response.context['postage_price'], 0)
        self.assertEqual(response.context['order_total'], 0)


class AddProductTestCase(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(
            slug = 'product-type',
            title = 'Test product type',
            price = Decimal(5.50),
            stand_alone = True,
        )
        self.product = Product.objects.create(
            product_type = self.product_type,
            stock_count = 10,
        )

    def test_error_adding_more_than_product_max_quantity_to_basket(self):
        response = self.client.post('/basket-add', data={
            'product_id': self.product.id,
            'quantity': 11,
        })
        self.assertContains(
            response,
            (
                "Can&#39;t add more than the maximum quantity to your basket. "
                "The maximum quantity for this product is 10."
            ),
            status_code=400,
        )

    def test_error_adding_sold_out_product_to_basket(self):
        self.product.sold_out = True
        self.product.save()
        response = self.client.post('/basket-add', data={
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.assertContains(
            response,
            (
                "This product is currently sold out, "
                "can&#39;t add it to your basket."
            ),
            status_code=400,
        )

    def test_can_add_less_than_product_max_quantity_to_basket(self):
        response = self.client.post('/basket-add', data={
            'product_id': self.product.id,
            'quantity': 10,
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_max_quantity_on_product_page(self):
        response = self.client.get('/product/product-type')
        self.assertContains(response, 'max="10"')