import uuid

from decimal import Decimal
from unittest import mock

from django.test import TestCase, override_settings
from django.core import mail

from mainapp.cart import Cart
from mainapp.models import (
    ProductType,
    Product,
    Order,
    OrderLine,
    OrderTransaction,
    OrderAddress,
)
from mainapp.views import _handle_order_transaction_success, _handle_order_transaction_failed


class OrderStartViewTestCase(TestCase):

    def setUp(self):
        product_type = ProductType.objects.create(
            slug = 'product-type1',
            title = 'Product Title',
            price = Decimal(12),
            stand_alone = True,
        )
        self.product = Product.objects.create(
            product_type = product_type,
        )

        session = self.client.session
        cart = Cart(session)
        cart.add(self.product, price=product_type.price, quantity=1)
        session.save()

    def test_basket_empty_redirect(self):
        session = self.client.session
        cart = Cart(session)
        cart.clear()
        session.save()

        response = self.client.get('/order-start')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_empty_customer_details_form(self):
        response = self.client.get('/order-start')
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(len(form.data), 0)
        field_keys = form.fields.keys()
        test_fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'billing_address1',
            'billing_2sserdda',
            'billing_3sserdda',
            'billing_4sserdda',
            'billing_city',
            'billing_state',
            'billing_post_code',
            'billing_country',
            'shipping_same',
            'shipping_name',
            'shipping_address1',
            'shipping_2sserdda',
            'shipping_3sserdda',
            'shipping_4sserdda',
            'shipping_city',
            'shipping_state',
            'shipping_post_code',
            'shipping_country',
            'mailinglist_subscribe',
        ]
        for test_field in test_fields:
            self.assertIn(test_field, field_keys)

    def test_customer_details_in_session_added_to_form(self):
        session = self.client.session
        session['customer_details'] = {
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'customer_phone': '0123456 888999',
            'billing_address': {
                'address1': 'Test address',
                'address2': '',
                'address3': '',
                'address4': '',
                'city': 'Some City',
                'state': 'A County',
                'post_code': 'AB12 3DE',
                'country': 'UK',
            }
        }
        session.save()

        response = self.client.get('/order-start')
        form = response.context['form']
        self.assertEqual(len(form.data), 11)
        self.assertEqual(form.data['customer_name'], 'Test Name')
        self.assertEqual(form.data['customer_email'], 'test@example.com')
        self.assertEqual(form.data['customer_phone'], '0123456 888999')
        self.assertEqual(form.data['billing_address1'], 'Test address')

    def test_error_phone_missing_international_delivery(self):
        response = self.client.post('/order-start', data={
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'billing_address1': 'Test address',
            'billing_city': 'Some City',
            'billing_state': 'A County',
            'billing_post_code': 'AB12 3DE',
            'billing_country': 'US',
        })
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('customer_phone', errors.keys())

    @mock.patch('mainapp.views.mailchimp_subscribe')
    def test_mailing_list_subscribe(self, patched_mailchimp_subscribe):
        response = self.client.post('/order-start', data={
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'billing_address1': 'Test address',
            'billing_city': 'Some City',
            'billing_state': 'A County',
            'billing_post_code': 'AB12 3DE',
            'billing_country': 'GB',
            'mailinglist_subscribe': True,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/order-payment')
        patched_mailchimp_subscribe.assert_called_once_with({
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'Name',
        }, 'orderform')

    @mock.patch('mainapp.views.mailchimp_subscribe')
    def test_order_created(self, patched_mailchimp_subscribe):
        self.assertEqual(Order.objects.count(), 0)

        response = self.client.post('/order-start', data={
            'customer_name': 'Test Name',
            'customer_email': 'test@example.com',
            'customer_phone': '012345 888999',
            'billing_address1': 'Test address',
            'billing_city': 'Some City',
            'billing_state': 'A County',
            'billing_post_code': 'AB12 3DE',
            'billing_country': 'GB',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/order-payment')

        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer_name, 'Test Name')
        self.assertEqual(order.customer_email, 'test@example.com')
        self.assertEqual(order.customer_phone, '012345 888999')


@override_settings(ADMINS=[])
class OrderTransactionTestCase(TestCase):

    def setUp(self):
        product_type = ProductType.objects.create(
            slug = 'product-type1',
            stand_alone = True,
        )

        self.product = Product.objects.create(
            product_type = product_type,
            stock_count = 3
        )

        self.customer_address = OrderAddress.objects.create(
            address1 = 'Test address 1',
            post_code = 'TESTPSTCODE',
            country = 'GB'
        )

        self.transaction_id = uuid.uuid4()
        self.order_id = uuid.uuid4()

        self.customer_name = 'Test name'
        self.customer_email = 'test@example.com'
        self.customer_phone = '012345 999888'

        self.order = Order.objects.create(
            unique_id = self.order_id,
            customer_name = self.customer_name,
            customer_email = self.customer_email,
            customer_phone = self.customer_phone,
            billing_address = self.customer_address,
            shipping_address = self.customer_address,
            state = 'notpaid'
        )

        self.orderline1 = OrderLine.objects.create(
            product = self.product,
            title = 'test product',
            item_price = '12.50',
            item_weight = 100,
            quantity = 2,
            order = self.order
        )

        # Orderlines without products should be handled correctly
        self.orderline2 = OrderLine.objects.create(
            title = 'test product 2',
            item_price = '5.50',
            item_weight = 50,
            quantity = 1,
            order = self.order
        )

        OrderTransaction.objects.create(
            unique_id = self.transaction_id,
            order = self.order,
            payment_processor = 'cardsave',
            state = 'started'
        )

        session = self.client.session
        session['order_id'] = str(self.order_id)
        session.save()

    def test_ordertransaction_failed(self):
        # AVS policy - Address verification
        ot = OrderTransaction.objects.get(unique_id=self.transaction_id)
        _handle_order_transaction_failed(ot, 'Card declined: AVS policy')

        self.assertIn('Please double check your billing address and try again', ot.message_info)

        # Test order-complete view
        response = self.client.get('/order-complete')
        self.assertIn('Order payment failed', str(response.content))
        self.assertIn('Card declined: AVS policy', str(response.content))
        self.assertIn('Please double check your billing address and try again', str(response.content))

        # Test payment failed email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Painting Dreams Order Payment Failed')
        self.assertIn('Card declined: AVS policy', mail.outbox[0].body)
        self.assertIn('Please double check your billing address and try again', mail.outbox[0].body)
        self.assertIn('Card declined: AVS policy', mail.outbox[0].alternatives[0][0])
        self.assertIn('Please double check your billing address and try again', mail.outbox[0].alternatives[0][0])

    def _test_order_email_content(self, email_content):
        self.assertIn(f'Order ID: {self.order_id}', email_content)
        orderline1_total = float(self.orderline1.item_price) * float(self.orderline1.quantity)
        orderline_text = (
            f'{self.orderline1.quantity} x '
            f'{self.orderline1.title} - '
            f'£{orderline1_total}'
        )
        self.assertIn(orderline_text, email_content)
        sub_total = float(orderline1_total) + float(self.orderline2.item_price)
        self.assertIn(f'Sub total: £{sub_total}', email_content)
        self.assertIn(self.customer_name, email_content)
        self.assertIn(self.customer_email, email_content)
        self.assertIn(self.customer_phone, email_content)
        self.assertIn(str(self.customer_address), email_content)

    def test_ordertransaction_success(self):
        ot = OrderTransaction.objects.get(unique_id=self.transaction_id)
        _handle_order_transaction_success(ot)

        # Test order-complete view
        response = self.client.get('/order-complete')
        self.assertIn('Order complete', str(response.content))
        self.assertIn(self.customer_name, str(response.content))
        self.assertIn(self.customer_email, str(response.content))
        self.assertIn(self.customer_phone, str(response.content))
        line_total = float(self.orderline1.item_price) * float(self.orderline1.quantity)
        orderline_text = (
            f'{self.orderline1.quantity} x '
            f'{self.orderline1.title} - '
            f'&pound;{line_total}'
        )
        self.assertIn(orderline_text, str(response.content))

        # Test product stock count reduced
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_count, 1)

        # Test order complete email
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Order received')
        self._test_order_email_content(mail.outbox[0].body)
        self._test_order_email_content(mail.outbox[0].alternatives[0][0])
        self.assertEqual(mail.outbox[1].subject, 'Painting Dreams Order')
        self._test_order_email_content(mail.outbox[1].body)
        self._test_order_email_content(mail.outbox[1].alternatives[0][0])

        # Test that if we re-run the same transaction
        # (where product.stock_count would be made negative)
        # we don't get any errors
        _handle_order_transaction_success(ot)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_count, 0)

        # Check that product has been marked sold out
        self.assertTrue(self.product.sold_out)

    def test_ordertransaction_cancelled(self):
        ot = OrderTransaction.objects.get(unique_id=self.transaction_id)
        ot.state = 'cancelled'
        ot.save()

        response = self.client.get('/order-complete')
        self.assertIn('Order payment cancelled', str(response.content))

    def test_ordertransaction_in_progress(self):
        ot = OrderTransaction.objects.get(unique_id=self.transaction_id)

        response = self.client.get('/order-complete')
        self.assertIn('Order in progress', str(response.content))
