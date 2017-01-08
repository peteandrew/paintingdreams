from copy import deepcopy
from unittest import mock
from urllib.parse import urlencode

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import reverse

from cardsave.models import PaymentResult
from cardsave.signals import payment_successful, payment_unsuccessful


@override_settings(ROOT_URLCONF='cardsave.tests.test_urls')
@override_settings(CARDSAVE_MERCHANT_ID = 'TestMerchantID')
@override_settings(CARDSAVE_CURRENCY_CODE = 826) # ISO 4217 GBP
@override_settings(CARDSAVE_ORDER_MODEL = 'cardsave.tests.models.Order')
@override_settings(CARDSAVE_PRESHARED_KEY = 'TestPresharedKey')
@override_settings(CARDSAVE_PASSWORD = 'TestPassword')
class PaymentResultTest(TestCase):

    RESULT_POST_PARAMS = {
        "HashDigest": 'd9df4c72d4c0a33112ccdd5a4d9374adb0369121',
        "MerchantID": settings.CARDSAVE_MERCHANT_ID,
        "StatusCode": 0,
        "Message": 'Test message',
        "PreviousStatusCode": 0,
        "PreviousMessage": ' ',
        "CrossReference": ' ',
        "Amount": 500, # £5 in pence
        "CurrencyCode": 826, # ISO 4217 GBP
        "OrderID": '1',
        "TransactionType": 'SALE',
        "TransactionDateTime": '2015-05-11 10:00:00 +00:00',
        "OrderDescription": 'Test description',
        "CustomerName": 'Test name',
        "Address1": 'Address line 1',
        "Address2": 'Address line 2',
        "Address3": 'Address line 3',
        "Address4": 'Address line 4',
        "City": 'TestCity',
        "State": 'TestState',
        "PostCode": 'APOSTCODE',
        "CountryCode": 826,
        "EmailAddress": 'test@example.com'
    }


    def do_post(self, post_params):
        with mock.patch('cardsave.tests.models.Order') as mock_order:
            mock_order.objects = mock.Mock()

            conf = {'get.return_value': mock.Mock(
                total_price = 5
            )}
            mock_order.objects.configure_mock(**conf)

            post_data = urlencode(post_params)
            response = self.client.post(reverse('cardsave-result'), post_data, content_type='application/x-www-form-urlencoded')

            self.assertEqual(response.status_code, 200)

            return response


    def assert_got_signal(self, signal, post_params):
        self.got_signal = False
        self.signal_obj = None

        def handle_signal(sender, **kwgargs):
            self.got_signal = True
            self.signal_obj = sender

        signal.connect(handle_signal)

        response = self.do_post(post_params)

        self.assertTrue(response.content.startswith(b'StatusCode=0'))

        payment_results = PaymentResult.objects.all()
        self.assertEqual(len(payment_results), 1)
        payment_result = payment_results[0]

        self.assertTrue(self.got_signal)
        self.assertEqual(self.signal_obj, payment_result)


    def test_payment_result_invalid_hash(self):
        result_post_params = deepcopy(self.RESULT_POST_PARAMS)
        result_post_params['HashDigest'] = 'InvalidHash'
        response = self.do_post(result_post_params)
        self.assertTrue(response.content.startswith(b'StatusCode=30'))
    

    def test_payment_successful_signal_received(self):
        self.assert_got_signal(payment_successful, self.RESULT_POST_PARAMS)


    def test_payment_unsuccessful_signal_received(self):
        result_post_params = deepcopy(self.RESULT_POST_PARAMS)
        result_post_params['StatusCode'] = 4
        result_post_params['HashDigest'] = '776c5a1c0a16f3b6af0f65ec8db1440b1be8cea8'
        self.assert_got_signal(payment_unsuccessful, result_post_params)
