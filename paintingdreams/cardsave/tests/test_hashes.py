import hashlib
from django.conf import settings
from django.test import TestCase, override_settings

from cardsave import cardsave_hash


class CardsavePaymentHashTestCase(TestCase):

    def setUp(self):
        class FakeField():
            initial = None
            def __init__(self, initial):
                self.initial = initial

        self.form_vals = {
            "EchoAVSCheckResult": FakeField(initial=False),
            "EchoCV2CheckResult": FakeField(initial=False),
            "EchoThreeDSecureAuthenticationCheckResult": FakeField(initial=False),
            "EchoCardType": FakeField(initial=False),
            "ThreeDSecureOverridePolicy": FakeField(initial=True),
            "CV2Mandatory": FakeField(initial=True),
            "Address1Mandatory": FakeField(initial=True),
            "CityMandatory": FakeField(initial=False),
            "PostCodeMandatory": FakeField(initial=True),
            "StateMandatory": FakeField(initial=False),
            "CountryMandatory": FakeField(initial=True),
            "EmailAddressEditable": FakeField(initial=False),
            "PhoneNumberEditable": FakeField(initial=False),
            "PaymentFormDisplaysResult": FakeField(initial=False),
            "ResultDeliveryMethod": FakeField(initial='SERVER'),
            "PhoneNumber": FakeField(initial=''),
            "TransactionType": FakeField(initial='SALE'),
            "TransactionDateTime": FakeField(initial='2015-05-11 10:00:00 +00:00')
        }

        self.initial_vals = {
            "Amount": 500, # £5 in pence
            "OrderID": '1',
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
            "EmailAddress": 'test@example.com',
            "CallbackURL": 'https://test.example.com/test-callback',
            "ServerResultURL": 'https://test.example.com/test-result'
        }
    
        self.correct_payment_hash = 'c46e9561e86fc820bd2908041b4aa5e7122a68f3'


    @override_settings(CARDSAVE_MERCHANT_ID = 'TestMerchantID')
    @override_settings(CARDSAVE_CURRENCY_CODE = 826) # ISO 4217 GBP
    @override_settings(CARDSAVE_PRESHARED_KEY = 'TestPresharedKey')
    @override_settings(CARDSAVE_PASSWORD = 'TestPassword')
    def test_cardsave_payment_hash_correct(self):
        self.assertEqual(cardsave_hash.payment_hash(self.form_vals, self.initial_vals), self.correct_payment_hash)


class CardsaveResultHashTestCase(TestCase):
    def setUp(self):
        self.form_vals = {
            'Amount': 500, # £5 in pence
            'OrderID': '1',
            'TransactionType': 'SALE',
            'TransactionDateTime': '2015-05-11 10:00:00 +00:00',
            'OrderDescription': 'Test description',
            'StatusCode': 0,
            'Message': 'Test message',
            'PreviousStatusCode': 0,
            'PreviousMessage': ' ',
            'CrossReference': ' ',
            'CustomerName': 'Test name',
            'Address1': 'Address line 1',
            'Address2': 'Address line 2',
            'Address3': 'Address line 3',
            'Address4': 'Address line 4',
            'City': 'TestCity',
            'State': 'TestState',
            'PostCode': 'APOSTCODE',
            'CountryCode': 826, # ISO 3166-1 UK
            'EmailAddress': 'test@example.com'
        }

        self.correct_result_hash = 'd9df4c72d4c0a33112ccdd5a4d9374adb0369121'

    @override_settings(CARDSAVE_MERCHANT_ID = 'TestMerchantID')
    @override_settings(CARDSAVE_CURRENCY_CODE = 826) # ISO 4217 GBP
    @override_settings(CARDSAVE_PRESHARED_KEY = 'TestPresharedKey')
    @override_settings(CARDSAVE_PASSWORD = 'TestPassword')
    def test_cardsave_result_hash_correct(self):
        self.assertEqual(cardsave_hash.result_hash(self.form_vals), self.correct_result_hash)


class CardsaveOutputHashTestCase(TestCase):
    def setUp(self):
        self.form_vals = {
            'OrderID': '1',
            'CrossReference': ' '
        }

        self.correct_output_hash = '7eb483c5e0b5ee020c9dff6152da9cca8b0b97cc'


    @override_settings(CARDSAVE_MERCHANT_ID = 'TestMerchantID')
    @override_settings(CARDSAVE_PRESHARED_KEY = 'TestPresharedKey')
    @override_settings(CARDSAVE_PASSWORD = 'TestPassword')
    def test_cardsave_result_hash_correct(self):
        self.assertEqual(cardsave_hash.output_hash(self.form_vals), self.correct_output_hash)
