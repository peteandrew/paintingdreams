from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit
from crispy_forms.bootstrap import FormActions


def products_table():
    html = """
        {% if product_errors|length > 0 %}
            <div class="product-errors">
            <ul>
            {% for error in product_errors %}
                <li>{{ error }}</li>
            {% endfor %}
            </ul>
            </div>
        {% endif %}
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
                    </td>
                    <td>&pound;{{ product.price }}</td>
                    <td>{% if not product.sold_out %}
                        <input class="textinput textInput form-control quantity" type="text" name="quantity_{{ product.code }}" min="0" value="{{ product.quantity }}">
                        <span style="display:none">{{ product.min_quantity }}</span>
                    {% endif %}</td>
                    <td>{% if not product.sold_out %}&pound{{ product.total }}{% endif %}</td>
                </tr>
            {% endfor %}
            </table>
        {% endfor %}
        <table class="wholesale_products">
            <tr>
                <td colspan="4">Sub total</td>
                <td class="colTotal">{{ subtotal }}</td>
            </tr>
        </table>
    """

    return html


def info():
    html = """
        <p class="wholesale-order-info">Cards have a minimum order quantity of 3.</p>
        <p class="wholesale-order-info">The minimum order amount is £50.</p>
        {% if postage_option == 'std' %}<p class="postage-info">For orders under £125 there is a delivery charge of £8. For orders of £125 and over there is no delivery charge.</p><p class="postage-info">For international orders, postage will be calculated depending on the weight of the order.</p>{% endif %}
        {% if postage_option == 'wghtcalc' %}<p class="postage-info">The carriage cost will be calculated depending on weight and you will be notified of the total cost before dispatch. Please confirm you are happy to proceed with the order once you have received the notification.</p>{% endif %}"""

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
    contact_tel = forms.CharField(required=False)

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
