import hashlib


def strip_invalid_chars(string):
    replace_chars = '#\><"[]'
    for char in replace_chars:
        string = string.replace(char, '')
    return string


def request_hash_digest(cardsave_settings,
                        order_details,
                        customer_details):

        hash_string = ('PreSharedKey=' + cardsave_settings['PreSharedKey'] + '&'
                       'MerchantID=' + cardsave_settings['MerchantID'] + '&'
                       'Password=' + cardsave_settings['Password'] + '&'
                       'Amount=' + order_details['Amount'] + '&'
                       'CurrencyCode=' + cardsave_settings['CurrencyCode'] + '&'
                       'EchoAVSCheckResult=' + cardsave_settings['EchoAVSCheckResult'] + '&'
                       'EchoCV2CheckResult=' + cardsave_settings['EchoCV2CheckResult'] + '&'
                       'EchoThreeDSecureAuthenticationCheckResult=' + cardsave_settings['EchoThreeDSecureAuthenticationCheckResult'] + '&'
                       'EchoCardType=' + cardsave_settings['EchoCardType'] + '&'
                       'AVSOverridePolicy=' + cardsave_settings['AVSOverridePolicy'] + '&'
                       'CV2OverridePolicy=' + cardsave_settings['CV2OverridePolicy'] + '&'
                       'ThreeDSecureOverridePolicy=' + cardsave_settings['ThreeDSecureOverridePolicy'] + '&'
                       'OrderID=' + order_details['OrderID'] + '&'
                       'TransactionType=' + cardsave_settings['TransactionType'] + '&'
                       'TransactionDateTime=' + order_details['TransactionDateTime'] + '&'
                       'CallbackURL=' + cardsave_settings['CallbackURL'] + '&'
                       'OrderDescription=' + order_details['OrderDescription'] + '&'
                       'CustomerName=' + customer_details['CustomerName'] + '&'
                       'Address1=' + customer_details['Address1'] + '&'
                       'Address2=' + customer_details['Address2'] + '&'
                       'Address3=' + customer_details['Address3'] + '&'
                       'Address4=' + customer_details['Address4'] + '&'
                       'City=' + customer_details['City'] + '&'
                       'State=' + customer_details['State'] + '&'
                       'PostCode=' + customer_details['PostCode'] + '&'
                       'CountryCode=' + customer_details['CountryCode'] + '&'
                       'EmailAddress=' + customer_details['EmailAddress'] + '&'
                       'PhoneNumber=' + customer_details['PhoneNumber'] + '&'
                       'EmailAddressEditable=' + cardsave_settings['EmailAddressEditable'] + '&'
                       'PhoneNumberEditable=' + cardsave_settings['PhoneNumberEditable'] + '&'
                       'CV2Mandatory=' + cardsave_settings['CV2Mandatory'] + '&'
                       'Address1Mandatory=' + cardsave_settings['Address1Mandatory'] + '&'
                       'CityMandatory=' + cardsave_settings['CityMandatory'] + '&'
                       'PostCodeMandatory=' + cardsave_settings['PostCodeMandatory'] + '&'
                       'StateMandatory=' + cardsave_settings['StateMandatory'] + '&'
                       'CountryMandatory=' + cardsave_settings['CountryMandatory'] + '&'
                       'ResultDeliveryMethod=' + cardsave_settings['ResultDeliveryMethod'] + '&'
                       'ServerResultURL=' + cardsave_settings['ServerResultURL'] + '&'
                       'PaymentFormDisplaysResult=' + cardsave_settings['PaymentFormDisplaysResult'])

        h = hashlib.sha1()
        h.update(hash_string.encode('utf-8'))
        return h.digest()


def cardsave_request(cardsave_settings,
                     order_details,
                     customer_details):

    for setting in cardsave_settings:
        cardsave_settings[setting] = strip_invalid_chars(cardsave_settings[setting])
    for detail in order_details:
        order_details[detail] = strip_invalid_chars(order_details[detail])
    for detail in customer_details:
        customer_details[detail] = strip_invalid_chars(customer_details[detail])

    hash_digest = request_hash_digest(cardsave_settings, order_details, customer_details)

    form = ('<form method="POST" action="' + cardsave_settings['cardsaveRequestURL'] + '">'
            '<input type="hidden" name="HashDigest" value="' + str(hash_digest) + '" />'
            '<input type="hidden" name="MerchantID" value="' + cardsave_settings['MerchantID'] + '" />'
            '<input type="hidden" name="Amount" value="' + order_details['Amount'] + '" />'
            '<input type="hidden" name="CurrencyCode" value="' + cardsave_settings['CurrencyCode'] + '" />'
            '<input type="hidden" name="EchoAVSCheckResult" value="' + cardsave_settings['EchoAVSCheckResult'] + '" />'
            '<input type="hidden" name="EchoCV2CheckResult" value="' + cardsave_settings['EchoCV2CheckResult'] + '" />'
            '<input type="hidden" name="EchoThreeDSecureAuthenticationCheckResult" value="' + cardsave_settings['EchoThreeDSecureAuthenticationCheckResult'] + '" />'
            '<input type="hidden" name="EchoCardType" value="' + cardsave_settings['EchoCardType'] + '" />'
            '<input type="hidden" name="AVSOverridePolicy" value="' + cardsave_settings['AVSOverridePolicy'] + '" />'
            '<input type="hidden" name="CV2OverridePolicy" value="' + cardsave_settings['CV2OverridePolicy'] + '" />'
            '<input type="hidden" name="ThreeDSecureOverridePolicy" value="' + cardsave_settings['ThreeDSecureOverridePolicy'] + '" />'
            '<input type="hidden" name="OrderID" value="' + order_details['OrderID'] + '" />'
            '<input type="hidden" name="TransactionType" value="' + cardsave_settings['TransactionType'] + '" />'
            '<input type="hidden" name="TransactionDateTime" value="' + order_details['TransactionDateTime'] + '" />'
            '<input type="hidden" name="CallbackURL" value="' + cardsave_settings['CallbackURL'] + '" />'
            '<input type="hidden" name="OrderDescription" value="' + order_details['OrderDescription'] + '" />'
            '<input type="hidden" name="CustomerName" value="' + customer_details['CustomerName'] + '" />'
            '<input type="hidden" name="Address1" value="' + customer_details['Address1'] + '" />'
            '<input type="hidden" name="Address2" value="' + customer_details['Address2'] + '" />'
            '<input type="hidden" name="Address3" value="' + customer_details['Address3'] + '" />'
            '<input type="hidden" name="Address4" value="' + customer_details['Address4'] + '" />'
            '<input type="hidden" name="City" value="' + customer_details['City'] + '" />'
            '<input type="hidden" name="State" value="' + customer_details['State'] + '" />'
            '<input type="hidden" name="PostCode" value="' + customer_details['PostCode'] + '" />'
            '<input type="hidden" name="CountryCode" value="' + customer_details['CountryCode'] + '" />'
            '<input type="hidden" name="EmailAddress" value="' + customer_details['EmailAddress'] + '" />'
            '<input type="hidden" name="PhoneNumber" value="' + customer_details['PhoneNumber'] + '" />'
            '<input type="hidden" name="EmailAddressEditable" value="' + cardsave_settings['EmailAddressEditable'] + '" />'
            '<input type="hidden" name="PhoneNumberEditable" value="' + cardsave_settings['PhoneNumberEditable'] + '" />'
            '<input type="hidden" name="CV2Mandatory" value="' + cardsave_settings['CV2Mandatory'] + '" />'
            '<input type="hidden" name="Address1Mandatory" value="' + cardsave_settings['Address1Mandatory'] + '" />'
            '<input type="hidden" name="CityMandatory" value="' + cardsave_settings['CityMandatory'] + '" />'
            '<input type="hidden" name="PostCodeMandatory" value="' + cardsave_settings['PostCodeMandatory'] + '" />'
            '<input type="hidden" name="StateMandatory" value="' + cardsave_settings['StateMandatory'] + '" />'
            '<input type="hidden" name="CountryMandatory" value="' + cardsave_settings['CountryMandatory'] + '" />'
            '<input type="hidden" name="ResultDeliveryMethod" value="' + cardsave_settings['ResultDeliveryMethod'] + '" />'
            '<input type="hidden" name="ServerResultURL" value="' + cardsave_settings['ServerResultURL'] + '" />'
            '<input type="hidden" name="PaymentFormDisplaysResult" value="' + cardsave_settings['PaymentFormDisplaysResult'] + '" />'
            '<input type="submit" value="Cardsave" />'
            '</form>')

    return form
