import logging
logger = logging.getLogger('django')

class PayPalFormNiceRenderer:

    def __init__(self, paypal_form):
        self.paypal_form = paypal_form

    def render(self):
        return self.paypal_form.render()
