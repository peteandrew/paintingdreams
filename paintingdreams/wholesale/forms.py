from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit
from crispy_forms.bootstrap import FormActions


def products_table():
    html = """
        {% for category, products in categories_products.items %}
            <h3>{{ category }}</h3>
            <table class="wholesale_products">
                <tr>
                    <th class="colCode">Code</th>
                    <th class="colTitle">Title</th>
                    <th class="colPrice">Price</th>
                    <th class="colQuantity">Quantity</th>
                    <th class="colTotal">Total</th>
                </tr>
            {% for product in products %}
                <tr {% if product.error %}class="error"{% endif %}>
                    <td>{{ product.code }}</td>
                    <td>
                        {{ product.title }}
                        {% if product.sold_out %}<span class="soldout">Currently sold out</span>{% endif %}
                        {% if product.new %}<span class="new">New</span>{% endif %}
                        {% if product.temporarily_unavailable %}<span class="soldout">Temporarily unavailable</span>{% endif %}
                    </td>
                    <td>&pound;{{ product.price }}</td>
                    <td>{% if not product.sold_out and not product.temporarily_unavailable %}
                        <input class="textinput textInput form-control quantity" type="text" name="quantity_{{ product.code }}" min="0" value="{{ product.quantity }}">
                        <span style="display:none">{{ product.min_quantity }}</span>
                    {% endif %}</td>
                    <td>{% if not product.sold_out and not product.temporarily_unavailable %}&pound{{ product.total }}{% endif %}</td>
                </tr>
            {% endfor %}
            </table>
        {% endfor %}
        <table class="wholesale_subtotal">
            <tr>
                <td>Sub total</td>
                <td>&pound;<span>{{ subtotal }}</span></td>
            </tr>
        </table>
    """

    return html


def info():
    html = """
        <p class="wholesale-order-info">Please note that all greetings card orders can now be placed via 'Love From The Artist'. Here is a link to my page on their website: <a href="https://www.lovefromtheartist.com/Artists/west-knoyle/painting-dreams" target="_blank">https://www.lovefromtheartist.com/Artists/west-knoyle/painting-dreams</a></p>
        <p class="wholesale-order-info">For all other items your order can be placed via this order form.</p>
        <p class="wholesale-order-info">Please contact me if you have any questions about the new ordering arrangement. info@paintingdreams.co.uk</p>
        <p class="wholesale-order-info">The minimum order is £50.</p>
        <p class="wholesale-order-info">For orders under £100 there is a delivery charge of £8.</p><p class="wholesale-order-info">For international orders, postage will be calculated depending on the weight of the order.</p>
        {% if postage_option == 'wghtcalc' %}<p class="wholesale-order-info">The carriage cost will be calculated depending on weight and you will be notified of the total cost before dispatch. Please confirm you are happy to proceed with the order once you have received the notification.</p>{% endif %}"""

    return html


def submit_button():
    html = """
        {% if create_order %}<input type="submit" name="submit" value="Create Order" class="btn btn-primary" id="submit-id-submit">{% else %}<input type="submit" name="submit" value="Update Order" class="btn btn-primary" id="submit-id-submit">{% endif %}"""

    return html


class ProductsForm(forms.Form):
    shop_name = forms.CharField(required=True)
    shop_address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':5}))
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    contact_tel = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(ProductsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'shop_name',
                'shop_address',
                'contact_name',
                'contact_email',
                'contact_tel'
            ),
            Fieldset(
                '',
                Div(
                    HTML(info())
                ),
            ),
            Fieldset(
                '',
                Div(
                    HTML(products_table())
                ),
            ),
            FormActions(
                HTML(submit_button())
            )
        )
