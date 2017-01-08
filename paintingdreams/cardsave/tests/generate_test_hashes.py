import hashlib


def payment_hash():

    vals = {
        "EchoAVSCheckResult": False,
        "EchoCV2CheckResult": False,
        "EchoThreeDSecureAuthenticationCheckResult": False,
        "EchoCardType": False,
        "ThreeDSecureOverridePolicy": True,
        "CV2Mandatory": True,
        "Address1Mandatory": True,
        "CityMandatory": False,
        "PostCodeMandatory": True,
        "StateMandatory": False,
        "CountryMandatory": True,
        "EmailAddressEditable": False,
        "PhoneNumberEditable": False,
        "PaymentFormDisplaysResult": False,
        "ResultDeliveryMethod": 'SERVER',
        "PhoneNumber": '',
        "TransactionType": 'SALE',
        "TransactionDateTime": '2015-05-11 10:00:00 +00:00',
        "CurrencyCode": 826, # ISO 4217 GBP
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
        "ServerResultURL": 'https://test.example.com/test-result',
        "MerchantID": 'TestMerchantID',
        "PreSharedKey": 'TestPresharedKey',
        "Password": 'TestPassword'
    }

    hash_string = ('PreSharedKey=' + vals['PreSharedKey'] + '&'
                   'MerchantID=' + vals['MerchantID'] + '&'
                   'Password=' + vals['Password'] + '&'
                   'Amount=' + str(vals['Amount']) + '&'
                   'CurrencyCode=' + str(vals['CurrencyCode']) + '&'
                   'EchoAVSCheckResult=' + str(vals['EchoAVSCheckResult']) + '&'
                   'EchoCV2CheckResult=' + str(vals['EchoCV2CheckResult']) + '&'
                   'EchoThreeDSecureAuthenticationCheckResult=' + str(vals['EchoThreeDSecureAuthenticationCheckResult']) + '&'
                   'EchoCardType=' + str(vals['EchoCardType']) + '&'
                   'ThreeDSecureOverridePolicy=' + str(vals['ThreeDSecureOverridePolicy']) + '&'
                   'OrderID=' + vals['OrderID'] + '&'
                   'TransactionType=' + vals['TransactionType'] + '&'
                   'TransactionDateTime=' + vals['TransactionDateTime'] + '&'
                   'CallbackURL=' + vals['CallbackURL'] + '&'
                   'OrderDescription=' + vals['OrderDescription'] + '&'
                   'CustomerName=' + vals['CustomerName'] + '&'
                   'Address1=' + vals['Address1'] + '&'
                   'Address2=' + vals['Address2'] + '&'
                   'Address3=' + vals['Address3'] + '&'
                   'Address4=' + vals['Address4'] + '&'
                   'City=' + vals['City'] + '&'
                   'State=' + vals['State'] + '&'
                   'PostCode=' + vals['PostCode'] + '&'
                   'CountryCode=' + str(vals['CountryCode']) + '&'
                   'EmailAddress=' + vals['EmailAddress'] + '&'
                   'PhoneNumber=' + vals['PhoneNumber'] + '&'
                   'EmailAddressEditable=' + str(vals['EmailAddressEditable']) + '&'
                   'PhoneNumberEditable=' + str(vals['PhoneNumberEditable']) + '&'
                   'CV2Mandatory=' + str(vals['CV2Mandatory']) + '&'
                   'Address1Mandatory=' + str(vals['Address1Mandatory']) + '&'
                   'CityMandatory=' + str(vals['CityMandatory']) + '&'
                   'PostCodeMandatory=' + str(vals['PostCodeMandatory']) + '&'
                   'StateMandatory=' + str(vals['StateMandatory']) + '&'
                   'CountryMandatory=' + str(vals['CountryMandatory']) + '&'
                   'ResultDeliveryMethod=' + vals['ResultDeliveryMethod'] + '&'
                   'ServerResultURL=' + vals['ServerResultURL'] + '&'
                   'PaymentFormDisplaysResult=' + str(vals['PaymentFormDisplaysResult']))

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    hashdigest = h.hexdigest()
    print('Payment hash: ' + hashdigest)


def result_hash1():
    vals = {
        "TransactionType": 'SALE',
        "TransactionDateTime": '2015-05-11 10:00:00 +00:00',
        "CurrencyCode": 826, # ISO 4217 GBP
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
        "MerchantID": 'TestMerchantID',
        "PreSharedKey": 'TestPresharedKey',
        "Password": 'TestPassword',
        "StatusCode": 0,
        "Message": 'Test message',
        "PreviousStatusCode": 0,
        "PreviousMessage": ' ',
        "CrossReference": ' ',
        "EmailAddress": 'test@example.com'
    }

    hash_string = ('PreSharedKey=' + vals['PreSharedKey'] + '&'
                   'MerchantID=' + vals['MerchantID'] + '&'
                   'Password=' + vals['Password'] + '&'
                   'StatusCode=' + str(vals['StatusCode']) + '&'
                   'Message=' + vals['Message'] + '&'
                   'PreviousStatusCode=' + str(vals['PreviousStatusCode']) + '&'
                   'PreviousMessage=' + vals['PreviousMessage'] + '&'
                   'CrossReference=' + vals['CrossReference'] + '&'
                   'AddressNumericCheckResult=&PostCodeCheckResult=&CV2CheckResult=&ThreeDSecureAuthenticationCheckResult=&CardType=&CardClass=&CardIssuer=&CardIssuerCountryCode=&'
                   'Amount=' + str(vals['Amount']) + '&'
                   'CurrencyCode=' + str(vals['CurrencyCode']) + '&'
                   'OrderID=' + vals['OrderID'] + '&'
                   'TransactionType=' + vals['TransactionType'] + '&'
                   'TransactionDateTime=' + vals['TransactionDateTime'] + '&'
                   'OrderDescription=' + vals['OrderDescription'] + '&'
                   'CustomerName=' + vals['CustomerName'] + '&'
                   'Address1=' + vals['Address1'] + '&'
                   'Address2=' + vals['Address2'] + '&'
                   'Address3=' + vals['Address3'] + '&'
                   'Address4=' + vals['Address4'] + '&'
                   'City=' + vals['City'] + '&'
                   'State=' + vals['State'] + '&'
                   'PostCode=' + vals['PostCode'] + '&'
                   'CountryCode=' + str(vals['CountryCode']) + '&'
                   'EmailAddress=' + vals['EmailAddress'] + '&'
                   'PhoneNumber=')

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    hashdigest = h.hexdigest()
    print('Result hash 1: ' + hashdigest)


def result_hash2():
    vals = {
        "TransactionType": 'SALE',
        "TransactionDateTime": '2015-05-11 10:00:00 +00:00',
        "CurrencyCode": 826, # ISO 4217 GBP
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
        "MerchantID": 'TestMerchantID',
        "PreSharedKey": 'TestPresharedKey',
        "Password": 'TestPassword',
        "StatusCode": 4,
        "Message": 'Test message',
        "PreviousStatusCode": 0,
        "PreviousMessage": ' ',
        "CrossReference": ' ',
        "EmailAddress": 'test@example.com'
    }

    hash_string = ('PreSharedKey=' + vals['PreSharedKey'] + '&'
                   'MerchantID=' + vals['MerchantID'] + '&'
                   'Password=' + vals['Password'] + '&'
                   'StatusCode=' + str(vals['StatusCode']) + '&'
                   'Message=' + vals['Message'] + '&'
                   'PreviousStatusCode=' + str(vals['PreviousStatusCode']) + '&'
                   'PreviousMessage=' + vals['PreviousMessage'] + '&'
                   'CrossReference=' + vals['CrossReference'] + '&'
                   'AddressNumericCheckResult=&PostCodeCheckResult=&CV2CheckResult=&ThreeDSecureAuthenticationCheckResult=&CardType=&CardClass=&CardIssuer=&CardIssuerCountryCode=&'
                   'Amount=' + str(vals['Amount']) + '&'
                   'CurrencyCode=' + str(vals['CurrencyCode']) + '&'
                   'OrderID=' + vals['OrderID'] + '&'
                   'TransactionType=' + vals['TransactionType'] + '&'
                   'TransactionDateTime=' + vals['TransactionDateTime'] + '&'
                   'OrderDescription=' + vals['OrderDescription'] + '&'
                   'CustomerName=' + vals['CustomerName'] + '&'
                   'Address1=' + vals['Address1'] + '&'
                   'Address2=' + vals['Address2'] + '&'
                   'Address3=' + vals['Address3'] + '&'
                   'Address4=' + vals['Address4'] + '&'
                   'City=' + vals['City'] + '&'
                   'State=' + vals['State'] + '&'
                   'PostCode=' + vals['PostCode'] + '&'
                   'CountryCode=' + str(vals['CountryCode']) + '&'
                   'EmailAddress=' + vals['EmailAddress'] + '&'
                   'PhoneNumber=')

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    hashdigest = h.hexdigest()
    print('Result hash 2: ' + hashdigest)


def output_hash():
    vals = {
        "MerchantID": 'TestMerchantID',
        "PreSharedKey": 'TestPresharedKey',
        "Password": 'TestPassword',
        "CrossReference": ' ',
        "OrderID": '1'
    }

    hash_string = ('PreSharedKey=' + vals['PreSharedKey'] + '&'
                   'MerchantID=' + vals['MerchantID'] + '&'
                   'Password=' + vals['Password'] + '&'
                   'CrossReference=' + vals['CrossReference'] + '&'
                   'OrderID=' + vals['OrderID'])

    h = hashlib.sha1()
    h.update(hash_string.encode('utf-8'))
    hashdigest = h.hexdigest()
    print('Output hash: ' + hashdigest)


payment_hash()
result_hash1()
result_hash2()
output_hash()
