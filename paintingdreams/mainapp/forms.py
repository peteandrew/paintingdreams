from django import forms

from django_countries import countries

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, Submit, HTML
from crispy_forms.bootstrap import FormActions


class OrderDetailsForm(forms.Form):
    customer_name = forms.CharField(label='Name', required=True)
    customer_email = forms.EmailField(label='Email', required=True)
    customer_phone = forms.CharField(label='Phone', required=False, help_text='Required for international deliveries')
    billing_address1 = forms.CharField(label='Line 1', required=True)
    billing_2sserdda = forms.CharField(label='Line 2', required=False)
    billing_3sserdda = forms.CharField(label='Line 3', required=False)
    billing_4sserdda = forms.CharField(label='Line 4', required=False)
    billing_city = forms.CharField(label='City', required=False)
    billing_state = forms.CharField(label='County / state', required=False)
    billing_post_code = forms.CharField(label='Post / zip code', required=False)
    billing_country = forms.ChoiceField(label='Country', required=True, choices=list(countries))
    shipping_different = forms.BooleanField(label='Delivery address different from above', required=False)
    shipping_name = forms.CharField(label='Name', required=False)
    shipping_address1 = forms.CharField(label='Line 1', required=False)
    shipping_2sserdda = forms.CharField(label='Line 2', required=False)
    shipping_3sserdda = forms.CharField(label='Line 3', required=False)
    shipping_4sserdda = forms.CharField(label='Line 4', required=False)
    shipping_city = forms.CharField(label='City', required=False)
    shipping_state = forms.CharField(label='County / state', required=False)
    shipping_post_code = forms.CharField(label='Post / zip code', required=False)
    shipping_country = forms.ChoiceField(label='Country', required=False, choices=list(countries))
    mailinglist_subscribe = forms.BooleanField(label='Subscribe to the Painting Dreams mailing list', required=False)
    remove_uk_only_products = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms customer-details'
        self.helper.form_method = 'post'
        self.helper.form_action = 'order-start'
        self.helper.layout = Layout(
            Div('customer_name', css_class='col-md-5'),
            Div(
                Div('customer_email', css_class='col-md-6'),
                Div('customer_phone', css_class='col-md-6'),
                css_class='col-md-12 row'
            ),
            Fieldset(
                'Billing address',
                HTML('<p class="help-block">Please ensure that address is entered on separate lines and that post / zip code is entered in the correct field</p>'),
                Div('billing_address1', css_class='col-md-6'),
                Div('billing_2sserdda', css_class='col-md-6'),
                Div('billing_3sserdda', css_class='col-md-6'),
                Div('billing_4sserdda', css_class='col-md-6'),
                Div('billing_city', css_class='col-md-6'),
                Div('billing_state', css_class='col-md-6'),
                Div(
                    Div('billing_post_code', css_class='col-md-4'),
                    css_class='col-md-12 row'
                ),
                Div(
                    Div('billing_country', css_class='col-md-4'),
                    css_class='col-md-12 row'
                ),
                css_class='col-md-12 row customer-details-address'
            ),
            Fieldset(
                'Delivery address',
                Div('shipping_different', css_class='col-md-12 row'),
                Div(
                    Div(
                        Div('shipping_name', css_class='col-md-6'),
                        css_class='col-md-12 row'
                    ),
                    Div('shipping_address1', css_class='col-md-6'),
                    Div('shipping_2sserdda', css_class='col-md-6'),
                    Div('shipping_3sserdda', css_class='col-md-6'),
                    Div('shipping_4sserdda', css_class='col-md-6'),
                    Div('shipping_city', css_class='col-md-6'),
                    Div('shipping_state', css_class='col-md-6'),
                    Div(
                        Div('shipping_post_code', css_class='col-md-6'),
                        css_class='col-md-12 row'
                    ),
                    Div(
                        Div('shipping_country', css_class='col-md-6'),
                        css_class='col-md-12 row'
                    ),
                    css_class='hidden',
                    css_id='delivery-address',
                ),
                css_class='col-sm-12 row customer-details-address',
            ),
            Fieldset(
                'Mailing list',
                'mailinglist_subscribe',
                css_class='col-sm-12 row order-mailinglist'
            ),
            Div(
                Div(
                    Submit('submit', 'Continue', css_class='btn-lg'),
                    css_class='col-sm-12',
                ),
                css_class='row',
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('customer_phone')
        if cleaned_data.get('shipping_address1'):
            shipping_country = cleaned_data.get('shipping_country')
        else:
            shipping_country = cleaned_data.get('billing_country')
        if shipping_country != 'GB' and len(phone.strip()) == 0:
            self.add_error('customer_phone', 'International destination has been selected, phone is required')


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
