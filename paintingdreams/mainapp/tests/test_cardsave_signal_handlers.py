from unittest import mock

from django.test import TestCase
from django.core import mail

import mainapp.views
from mainapp.models import Order, OrderAddress
from cardsave.signals import payment_successful, payment_unsuccessful


class PaymentHandlerTest(TestCase):


    def setUp(self):
        customer_address = OrderAddress.objects.create(
            address1 = 'Test address 1',
            post_code = 'TESTPSTCODE',
            country = 'GB'
        )

        self.order = Order.objects.create(
            unique_id = '1',
            customer_name = 'Test name',
            customer_email = 'test@example.com',
            customer_billing_address = customer_address,
            customer_shipping_address = customer_address,
            total_price = 12.5,
            payment_processor = 'cardsave',
            state = 'payment_started'
        )


    def test_success_order_updated(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = '1'
            )
            payment_successful.send(sender=mock_payment_result)

            self.assertEqual(Order.objects.all()[0].state, 'payment_complete')


    def test_success_emails_sent(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = '1'
            )
            payment_successful.send(sender=mock_payment_result)

            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[0].subject, 'Order received')


    def test_unsuccess_order_updated(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = '1'
            )
            payment_unsuccessful.send(sender=mock_payment_result)

            self.assertEqual(Order.objects.all()[0].state, 'payment_failed')


    def test_unsuccess_emails_sent(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = '1'
            )
            payment_unsuccessful.send(sender=mock_payment_result)

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Painting Dreams Order Payment Failed')
