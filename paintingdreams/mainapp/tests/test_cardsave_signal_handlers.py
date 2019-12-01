import uuid

from unittest import mock

from django.test import TestCase, override_settings
from django.core import mail

import mainapp.views
from mainapp.models import Order, OrderLine, OrderTransaction, OrderAddress
from cardsave.signals import payment_successful, payment_unsuccessful


@override_settings(ADMINS=[])
class PaymentHandlerTest(TestCase):


    def setUp(self):
        customer_address = OrderAddress.objects.create(
            address1 = 'Test address 1',
            post_code = 'TESTPSTCODE',
            country = 'GB'
        )

        self.unique_id = uuid.uuid4()

        self.order = Order.objects.create(
            customer_name = 'Test name',
            customer_email = 'test@example.com',
            billing_address = customer_address,
            shipping_address = customer_address,
            state = 'notpaid'
        )

        OrderLine.objects.create(
            title = 'test product',
            item_price = '12.50',
            item_weight = 100,
            quantity = 1,
            order = self.order
        )

        OrderTransaction.objects.create(
            unique_id = self.unique_id,
            order = self.order,
            payment_processor = 'cardsave',
            state = 'started'
        )


    def test_success_order_updated(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = self.unique_id
            )
            payment_successful.send(sender=mock_payment_result)

            self.assertEqual(Order.objects.all()[0].state, 'paid')
            self.assertEqual(OrderTransaction.objects.all()[0].state, 'complete')


    def test_success_emails_sent(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = self.unique_id
            )
            payment_successful.send(sender=mock_payment_result)

            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(mail.outbox[0].subject, 'Order received')


    def test_unsuccess_order_updated(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = self.unique_id,
                message = 'failure message'
            )
            payment_unsuccessful.send(sender=mock_payment_result)

            self.assertEqual(Order.objects.all()[0].state, 'notpaid')
            self.assertEqual(OrderTransaction.objects.all()[0].state, 'failed')


    def test_unsuccess_emails_sent(self):
        with mock.patch('cardsave.models.PaymentResult') as mock_payment_result:
            mock_payment_result = mock.Mock(
                order_id = self.unique_id,
                message = 'failure message'
            )
            payment_unsuccessful.send(sender=mock_payment_result)

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Painting Dreams Order Payment Failed')
