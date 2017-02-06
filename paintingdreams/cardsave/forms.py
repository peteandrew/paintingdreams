from datetime import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

from cardsave import cardsave_hash


class CardsavePaymentForm(forms.Form):
    EchoAVSCheckResult = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    EchoCV2CheckResult = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    EchoThreeDSecureAuthenticationCheckResult = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    EchoCardType = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    ThreeDSecureOverridePolicy = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    CV2Mandatory = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    Address1Mandatory = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    CityMandatory = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    PostCodeMandatory = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    StateMandatory = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    CountryMandatory = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    EmailAddressEditable = forms.BooleanField(widget=forms.HiddenInput, initial=False)
    PhoneNumberEditable = forms.BooleanField(widget=forms.HiddenInput, initial=False)

    PaymentFormDisplaysResult = forms.BooleanField(widget=forms.HiddenInput, initial=False)

    ResultDeliveryMethod = forms.ChoiceField(
        choices=[('POST', 'post'), ('SERVER', 'server'), ('SERVER_PULL', 'server pull')],
        widget=forms.HiddenInput,
        initial='SERVER')

    HashDigest = forms.CharField(widget=forms.HiddenInput)

    MerchantID = forms.CharField(widget=forms.HiddenInput, initial=settings.CARDSAVE_MERCHANT_ID)

    Amount = forms.IntegerField(widget=forms.HiddenInput)
    CurrencyCode = forms.IntegerField(widget=forms.HiddenInput, initial=settings.CARDSAVE_CURRENCY_CODE)

    OrderID = forms.CharField(widget=forms.HiddenInput)
    OrderDescription = forms.CharField(widget=forms.HiddenInput, initial='')

    CustomerName = forms.CharField(widget=forms.HiddenInput, initial='')
    Address1 = forms.CharField(widget=forms.HiddenInput, initial='')
    Address2 = forms.CharField(widget=forms.HiddenInput, initial='')
    Address3 = forms.CharField(widget=forms.HiddenInput, initial='')
    Address4 = forms.CharField(widget=forms.HiddenInput, initial='')
    City = forms.CharField(widget=forms.HiddenInput, initial='')
    State = forms.CharField(widget=forms.HiddenInput, initial='')
    PostCode = forms.CharField(widget=forms.HiddenInput, initial='')
    CountryCode = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    EmailAddress = forms.EmailField(widget=forms.HiddenInput, initial='')
    PhoneNumber = forms.CharField(widget=forms.HiddenInput, initial='')

    TransactionType = forms.ChoiceField(
        choices=[('SALE', 'sale'), ('PREAUTH', 'preauth')],
        widget=forms.HiddenInput,
        initial='SALE')
    TransactionDateTime = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S +00:00'],
        widget=forms.HiddenInput)

    CallbackURL = forms.URLField(widget=forms.HiddenInput)
    ServerResultURL = forms.URLField(widget=forms.HiddenInput)


    def __init__(self, *args, **kwargs):
        super(CardsavePaymentForm, self).__init__(*args, **kwargs)
        self.fields['TransactionDateTime'].initial = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +00:00')
        self.fields['HashDigest'].initial = cardsave_hash.payment_hash(self.fields, self.initial)


    def render(self):
        return mark_safe(
            u"""<form method="post" action="%s">%s<button type="submit" class="btn btn-primary btn-lg">Continue to Cardsave</button></form>""" % (
                settings.CARDSAVE_REQUEST_URL, self.as_p()))


class CardsaveResultForm(forms.Form):
    HashDigest = forms.CharField(widget=forms.HiddenInput)
    MerchantID = forms.CharField(widget=forms.HiddenInput)
    StatusCode = forms.IntegerField(widget=forms.HiddenInput)
    Message = forms.CharField(widget=forms.HiddenInput, required=False)
    PreviousStatusCode = forms.IntegerField(widget=forms.HiddenInput, required=False)
    PreviousMessage = forms.CharField(widget=forms.HiddenInput, required=False)
    CrossReference = forms.CharField(widget=forms.HiddenInput, required=False)
    Amount = forms.DecimalField(decimal_places=2, widget=forms.HiddenInput)
    CurrencyCode = forms.IntegerField(widget=forms.HiddenInput)
    OrderID = forms.CharField(widget=forms.HiddenInput)
    TransactionType = forms.ChoiceField(
        choices=[('SALE', 'sale'), ('PREAUTH', 'preauth')],
        widget=forms.HiddenInput)
    TransactionDateTime = forms.CharField(widget=forms.HiddenInput)
    OrderDescription = forms.CharField(widget=forms.HiddenInput, required=False)
    CustomerName = forms.CharField(widget=forms.HiddenInput, required=False)
    Address1 = forms.CharField(widget=forms.HiddenInput, required=False)
    Address2 = forms.CharField(widget=forms.HiddenInput, required=False)
    Address3 = forms.CharField(widget=forms.HiddenInput, required=False)
    Address4 = forms.CharField(widget=forms.HiddenInput, required=False)
    City = forms.CharField(widget=forms.HiddenInput, required=False)
    State = forms.CharField(widget=forms.HiddenInput, required=False)
    PostCode = forms.CharField(widget=forms.HiddenInput, required=False)
    CountryCode = forms.IntegerField(widget=forms.HiddenInput)
    EmailAddress = forms.CharField(widget=forms.HiddenInput, required=False)


class CardsaveOutputForm(forms.Form):
    HashDigest = forms.CharField(widget=forms.HiddenInput)
    MerchantID = forms.CharField(widget=forms.HiddenInput)
    CrossReference = forms.CharField(widget=forms.HiddenInput)
    OrderID = forms.CharField(widget=forms.HiddenInput)
