from django import forms

from django_countries import countries

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, HTML
from crispy_forms.bootstrap import FormActions


class OrderDetailsForm(forms.Form):
    customer_name = forms.CharField(required=True)
    customer_email = forms.EmailField(required=True)
    billing_address1 = forms.CharField(label='Line 1', required=True)
    billing_address2 = forms.CharField(label='Line 2', required=False)
    billing_address3 = forms.CharField(label='Line 3', required=False)
    billing_address4 = forms.CharField(label='Line 4', required=False)
    billing_city = forms.CharField(label='City', required=False)
    billing_state = forms.CharField(label='County / state', required=False)
    billing_post_code = forms.CharField(label='Post / zip code', required=False)
    billing_country = forms.ChoiceField(label='Country', required=True, choices=list(countries))
    shipping_same = forms.BooleanField(label='Same as above', required=False)
    shipping_name = forms.CharField(label='Name', required=False)
    shipping_address1 = forms.CharField(label='Line 1', required=False)
    shipping_address2 = forms.CharField(label='Line 2', required=False)
    shipping_address3 = forms.CharField(label='Line 3', required=False)
    shipping_address4 = forms.CharField(label='Line 4', required=False)
    shipping_city = forms.CharField(label='City', required=False)
    shipping_state = forms.CharField(label='County / state', required=False)
    shipping_post_code = forms.CharField(label='Post / zip code', required=False)
    shipping_country = forms.ChoiceField(label='Country', required=False, choices=list(countries))
    mailinglist_subscribe = forms.BooleanField(label='Subscribe to the Painting Dreams mailing list', required=False)

    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms form-horizontal customer-details'
        self.helper.form_method = 'post'
        self.helper.form_action = 'order-start'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'customer_name',
                'customer_email'
            ),
            Fieldset(
                'Billing address',
                HTML('<p class="larger-text">Please ensure that address is entered on separate lines and that post / zip code is entered in the correct field</p>'),
                'billing_address1',
                'billing_address2',
                'billing_address3',
                'billing_address4',
                'billing_city',
                'billing_state',
                'billing_post_code',
                'billing_country'
            ),
            Fieldset(
                'Delivery address',
                HTML('<p>If different from above</p>'),
                'shipping_name',
                'shipping_address1',
                'shipping_address2',
                'shipping_address3',
                'shipping_address4',
                'shipping_city',
                'shipping_state',
                'shipping_post_code',
                'shipping_country'
            ),
            Fieldset(
                'Mailing list',
                'mailinglist_subscribe',
                css_class='order-mailinglist'
            ),
            Div(
                Div(
                    Submit('submit', 'Continue', css_class='btn btn-primary, btn-lg',),
                    css_class='col-sm-12',
                ),
                css_class='row',
            )
        )


class MailingListSubscribeForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(MailingListSubscribeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms form-horizontal mailinglist'
        self.helper.form_method = 'post'
        self.helper.form_action = 'mailinglist'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'last_name',
                'email'
            ),
            HTML('<div class="g-recaptcha" data-sitekey="6LcmtCwUAAAAAGqO-FTeSSi6mqrRUxfROecra4Gf"></div>'),
            Div(
                Div(
                    Submit('submit', 'Subscribe', css_class='btn btn-primary, btn-lg',),
                    css_class='col-sm-12',
                ),
                css_class='row',
            )
        )
