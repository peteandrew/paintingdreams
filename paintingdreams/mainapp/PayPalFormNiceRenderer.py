from django.utils.html import format_html

class PayPalFormNiceRenderer:

    def __init__(self, paypal_form):
        self.paypal_form = paypal_form

    def render(self):
        return format_html(u"""<form action="{0}" method="post">
            {1}
            <button type="submit" class="btn btn-primary btn-lg">Continue to PayPal</button>
            </form>""", self.paypal_form.get_endpoint(), self.paypal_form.as_p())
