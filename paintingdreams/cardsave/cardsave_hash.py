import hashlib

from django.conf import settings


def field_value(field_name, form_vals, initial_vals):
    if field_name in initial_vals:
        return str(initial_vals[field_name])
    else:
        return str(form_vals[field_name].initial)


def payment_hash(form_vals, initial_vals):
    hash_string = ('PreSharedKey=' + settings.CARDSAVE_PRESHARED_KEY + '&'
                   'MerchantID=' + settings.CARDSAVE_MERCHANT_ID + '&'
                   'Password=' + settings.CARDSAVE_PASSWORD + '&'
                   'Amount=' + field_value('Amount', form_vals, initial_vals) + '&'
                   'CurrencyCode=' + str(settings.CARDSAVE_CURRENCY_CODE) + '&'
                   'EchoAVSCheckResult=' + field_value('EchoAVSCheckResult', form_vals, initial_vals) + '&'
                   'EchoCV2CheckResult=' + field_value('EchoCV2CheckResult', form_vals, initial_vals) + '&'
                   'EchoThreeDSecureAuthenticationCheckResult=' + field_value('EchoThreeDSecureAuthenticationCheckResult', form_vals, initial_vals) + '&'
                   'EchoCardType=' + field_value('EchoCardType', form_vals, initial_vals) + '&'
                   'ThreeDSecureOverridePolicy=' + field_value('ThreeDSecureOverridePolicy', form_vals, initial_vals) + '&'
                   'OrderID=' + field_value('OrderID', form_vals, initial_vals) + '&'
                   'TransactionType=' + field_value('TransactionType', form_vals, initial_vals) + '&'
                   'TransactionDateTime=' + field_value('TransactionDateTime', form_vals, initial_vals) + '&'
                   'CallbackURL=' + field_value('CallbackURL', form_vals, initial_vals) + '&'
                   'OrderDescription=' + field_value('OrderDescription', form_vals, initial_vals) + '&'
                   'CustomerName=' + field_value('CustomerName', form_vals, initial_vals) + '&'
                   'Address1=' + field_value('Address1', form_vals, initial_vals) + '&'
                   'Address2=' + field_value('Address2', form_vals, initial_vals) + '&'
                   'Address3=' + field_value('Address3', form_vals, initial_vals) + '&'
                   'Address4=' + field_value('Address4', form_vals, initial_vals) + '&'
                   'City=' + field_value('City', form_vals, initial_vals) + '&'
                   'State=' + field_value('State', form_vals, initial_vals) + '&'
                   'PostCode=' + field_value('PostCode', form_vals, initial_vals) + '&'
                   'CountryCode=' + field_value('CountryCode', form_vals, initial_vals) + '&'
                   'EmailAddress=' + field_value('EmailAddress', form_vals, initial_vals) + '&'
                   'PhoneNumber=' + field_value('PhoneNumber', form_vals, initial_vals) + '&'
                   'EmailAddressEditable=' + field_value('EmailAddressEditable', form_vals, initial_vals) + '&'
                   'PhoneNumberEditable=' + field_value('PhoneNumberEditable', form_vals, initial_vals) + '&'
                   'CV2Mandatory=' + field_value('CV2Mandatory', form_vals, initial_vals) + '&'
                   'Address1Mandatory=' + field_value('Address1Mandatory', form_vals, initial_vals) + '&'
                   'CityMandatory=' + field_value('CityMandatory', form_vals, initial_vals) + '&'
                   'PostCodeMandatory=' + field_value('PostCodeMandatory', form_vals, initial_vals) + '&'
                   'StateMandatory=' + field_value('StateMandatory', form_vals, initial_vals) + '&'
                   'CountryMandatory=' + field_value('CountryMandatory', form_vals, initial_vals) + '&'
                   'ResultDeliveryMethod=' + field_value('ResultDeliveryMethod', form_vals, initial_vals) + '&'
                   'ServerResultURL=' + field_value('ServerResultURL', form_vals, initial_vals) + '&'
                   'PaymentFormDisplaysResult=' + field_value('PaymentFormDisplaysResult', form_vals, initial_vals))

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    return h.hexdigest()


def result_hash(form_vals):
    hash_string = ('PreSharedKey=' + settings.CARDSAVE_PRESHARED_KEY + '&'
                   'MerchantID=' + settings.CARDSAVE_MERCHANT_ID + '&'
                   'Password=' + settings.CARDSAVE_PASSWORD + '&'
                   'StatusCode=' + str(form_vals['StatusCode']) + '&'
                   'Message=' + form_vals['Message'] + '&'
                   'PreviousStatusCode=')
    if form_vals['PreviousStatusCode'] is not None:
        hash_string += str(form_vals['PreviousStatusCode'])
    hash_string += '&'
    hash_string += ('PreviousMessage=' + form_vals['PreviousMessage'] + '&'
                    'CrossReference=' + form_vals['CrossReference'] + '&'
                    'AddressNumericCheckResult=&PostCodeCheckResult=&CV2CheckResult=&ThreeDSecureAuthenticationCheckResult=&CardType=&CardClass=&CardIssuer=&CardIssuerCountryCode=&'
                    'Amount=' + str(form_vals['Amount']) + '&'
                    'CurrencyCode=' + str(settings.CARDSAVE_CURRENCY_CODE) + '&'
                    'OrderID=' + form_vals['OrderID'] + '&'
                    'TransactionType=' + form_vals['TransactionType'] + '&'
                    'TransactionDateTime=' + str(form_vals['TransactionDateTime']) + '&'
                    'OrderDescription=' + form_vals['OrderDescription'] + '&'
                    'CustomerName=' + form_vals['CustomerName'] + '&'
                    'Address1=' + form_vals['Address1'] + '&'
                    'Address2=' + form_vals['Address2'] + '&'
                    'Address3=' + form_vals['Address3'] + '&'
                    'Address4=' + form_vals['Address4'] + '&'
                    'City=' + form_vals['City'] + '&'
                    'State=' + form_vals['State'] + '&'
                    'PostCode=' + form_vals['PostCode'] + '&'
                    'CountryCode=' + str(form_vals['CountryCode']) + '&'
                    'EmailAddress=' + form_vals['EmailAddress'] + '&'
                    'PhoneNumber=')

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    return h.hexdigest()


def output_hash(form_vals):
    hash_string = ('PreSharedKey=' + settings.CARDSAVE_PRESHARED_KEY + '&'
                   'MerchantID=' + settings.CARDSAVE_MERCHANT_ID + '&'
                   'Password=' + settings.CARDSAVE_PASSWORD + '&'
                   'CrossReference=' + form_vals['CrossReference'] + '&'
                   'OrderID=' + form_vals['OrderID'])

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    return h.hexdigest()

