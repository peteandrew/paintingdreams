from unittest import mock
from django.conf import settings
from django.test import TestCase, override_settings

from cardsave.forms import CardsavePaymentForm


class CardsavePaymentFormTestCase(TestCase):
    def setUp(self):
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
            "CountryCode": 100,
            "EmailAddress": 'test@example.com',
            "CallbackURL": 'https://test.example.com/test-callback',
            "ServerResultURL": 'https://test.example.com/test-result'
        }


    @mock.patch('cardsave.forms.cardsave_hash')
    @override_settings(CARDSAVE_MERCHANT_ID = 'TestMerchantID')
    @override_settings(CARDSAVE_CURRENCY_CODE = 826) # ISO 4217 GBP
    @override_settings(CARDSAVE_REQUEST_URL = 'https://testcardsaveurl.com')
    def test_cardsave_payment_form_render(self, mock_cardsave_hash):
        testhashdigest = 'testhashdigest'
        mock_cardsave_hash.payment_hash.return_value = testhashdigest

        form = CardsavePaymentForm(initial=self.initial_vals)
        form_html = form.render()

        """ Complete check for <form> <input name="HashDigest"> </form> tags as these are the only we are adding
            in CardsavePaymentForm. All others are added by the Form super class. We only check that these
            exist. """
        self.assertTrue(form_html.startswith('<form method="post" action="' + settings.CARDSAVE_REQUEST_URL + '">'))
        self.assertIn('<input id="id_HashDigest" name="HashDigest" type="hidden" value="' + testhashdigest + '" />', form_html)
        self.assertIn('name="MerchantID"', form_html)
        self.assertIn('name="Amount"', form_html)
        self.assertIn('name="CurrencyCode"', form_html)
        self.assertIn('name="EchoAVSCheckResult"', form_html)
        self.assertIn('name="EchoCV2CheckResult"', form_html)
        self.assertIn('name="EchoThreeDSecureAuthenticationCheckResult"', form_html)
        self.assertIn('name="EchoCardType"', form_html)
        self.assertIn('name="ThreeDSecureOverridePolicy"', form_html)
        self.assertIn('name="OrderID"', form_html)
        self.assertIn('name="TransactionType"', form_html)
        self.assertIn('name="TransactionDateTime"', form_html)
        self.assertIn('name="CallbackURL"', form_html)
        self.assertIn('name="OrderDescription"', form_html)
        self.assertIn('name="CustomerName"', form_html)
        self.assertIn('name="Address1"', form_html)
        self.assertIn('name="Address2"', form_html)
        self.assertIn('name="Address3"', form_html)
        self.assertIn('name="Address4"', form_html)
        self.assertIn('name="City"', form_html)
        self.assertIn('name="State"', form_html)
        self.assertIn('name="PostCode"', form_html)
        self.assertIn('name="CountryCode"', form_html)
        self.assertIn('name="EmailAddress"', form_html)
        self.assertIn('name="PhoneNumber"', form_html)
        self.assertIn('name="EmailAddressEditable"', form_html)
        self.assertIn('name="PhoneNumberEditable"', form_html)
        self.assertIn('name="CV2Mandatory"', form_html)
        self.assertIn('name="Address1Mandatory"', form_html)
        self.assertIn('name="CityMandatory"', form_html)
        self.assertIn('name="PostCodeMandatory"', form_html)
        self.assertIn('name="StateMandatory"', form_html)
        self.assertIn('name="CountryMandatory"', form_html)
        self.assertIn('name="ResultDeliveryMethod"', form_html)
        self.assertIn('name="ServerResultURL"', form_html)
        self.assertIn('name="PaymentFormDisplaysResult"', form_html)
        self.assertTrue(form_html.endswith('</form>'))
