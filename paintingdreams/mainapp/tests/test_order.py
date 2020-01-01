import uuid

from django.test import TestCase, override_settings
from django.core import mail

from mainapp.models import Order, OrderLine, OrderTransaction, OrderAddress
from mainapp.views import _handle_order_transaction_success, _handle_order_transaction_failed


@override_settings(ADMINS=[])
class OrderTestCase(TestCase):

    def setUp(self):
        self.customer_address = OrderAddress.objects.create(
            address1 = 'Test address 1',
            post_code = 'TESTPSTCODE',
            country = 'GB'
        )

        self.transaction_id = uuid.uuid4()
        self.order_id = uuid.uuid4()

        self.customer_name = 'Test name'
        self.customer_email = 'test@example.com'

        self.order = Order.objects.create(
            unique_id = self.order_id,
            customer_name = self.customer_name,
            customer_email = self.customer_email,
            billing_address = self.customer_address,
            shipping_address = self.customer_address,
            state = 'notpaid'
        )

        self.orderline1 = OrderLine.objects.create(
            title = 'test product',
            item_price = '12.50',
            item_weight = 100,
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
        orderline_text = (
            f'{self.orderline1.quantity} x '
            f'{self.orderline1.title} - '
            f'£{self.orderline1.item_price}'
        )
        self.assertIn(orderline_text, email_content)
        self.assertIn(f'Sub total: £{self.orderline1.item_price}', email_content)
        self.assertIn(self.customer_name, email_content)
        self.assertIn(self.customer_email, email_content)
        self.assertIn(str(self.customer_address), email_content)

    def test_ordertransaction_success(self):
        ot = OrderTransaction.objects.get(unique_id=self.transaction_id)
        _handle_order_transaction_success(ot)

        # Test order-complete view
        response = self.client.get('/order-complete')
        self.assertIn('Order complete', str(response.content))
        self.assertIn(self.customer_name, str(response.content))
        self.assertIn(self.customer_email, str(response.content))
        orderline_text = (
            f'{self.orderline1.quantity} x '
            f'{self.orderline1.title} - '
            f'&pound;{self.orderline1.item_price}'
        )
        self.assertIn(orderline_text, str(response.content))

        # Test order complete email
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Order received')
        self._test_order_email_content(mail.outbox[0].body)
        self._test_order_email_content(mail.outbox[0].alternatives[0][0])
        self.assertEqual(mail.outbox[1].subject, 'Painting Dreams Order')
        self._test_order_email_content(mail.outbox[1].body)
        self._test_order_email_content(mail.outbox[1].alternatives[0][0])

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