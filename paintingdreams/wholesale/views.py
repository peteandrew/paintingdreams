from collections import OrderedDict

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.mail import send_mail, mail_admins

from wholesale.forms import ProductsForm
from wholesale.models import Product, Category, Special, SpecialProductRemoved, Order, OrderLine

def get_categories_products(products_removed):
    categories_products = OrderedDict()

    categories = Category.objects.order_by('title')
    for category in categories:
        products_temp = Product.objects.filter(category=category).order_by('code')
        if len(products_temp) < 1:
            continue
        categories_products[category] = []
        for product in products_temp:
            found = False
            for removed_product in products_removed:
                if removed_product.product == product:
                    found = True
            if found: continue
            categories_products[category].append(product)

    return categories_products


def start(request, special_name):
    special = None
    products_removed = []
    postage_option = 'none'
    product_errors = []
    display_vat_message = True
    display_brexit_message = False

    if len(special_name) > 0:
        try:
            special = Special.objects.get(name=special_name)
            products_removed = SpecialProductRemoved.objects.filter(
                special=special).all()
            postage_option = special.postage_option
            display_vat_message = special.display_vat_message
            display_brexit_message = special.display_brexit_message
        except Special.DoesNotExist:
            raise Http404("Special form %s does not exist" % (special_name,))

    categories_products = get_categories_products(products_removed)

    try:
        order_details = request.session['wholesale_order']
        form = ProductsForm(order_details)
        create_order = False
    except KeyError:
        order_details = {}
        form = ProductsForm()
        create_order = True

    order_subtotal = 0

    for cat_products in categories_products.values():
        for product in cat_products:
            if product.sold_out or product.temporarily_unavailable:
                continue

            key = 'quantity_' + product.code

            if request.method == 'POST':
                if key in order_details:
                    del order_details[key]

                try:
                    quantity = int(request.POST[key])
                except ValueError:
                    quantity = 0

                if quantity > 0:
                    order_details[key] = quantity

                    if quantity < product.min_quantity:
                        product.error = True
                        product_errors.append('Quantity entered for ' + product.code + ' - ' + product.title + ' less than minimum quantity: ' + str(product.min_quantity))

                    order_subtotal += product.price * quantity

            if key in order_details:
                product.quantity = order_details[key]
                product.total = product.price * order_details[key]
            else:
                product.quantity = 0
                product.total = 0

    if request.method == 'POST':
        form = ProductsForm(request.POST)

        if form.is_valid():
            order_details['shop_name'] = form.cleaned_data['shop_name']
            order_details['shop_address'] = form.cleaned_data['shop_address']
            order_details['contact_name'] = form.cleaned_data['contact_name']
            order_details['contact_email'] = form.cleaned_data['contact_email']
            order_details['contact_tel'] = form.cleaned_data['contact_tel']
        else:
            product_errors.append('Required field is missing or invalid')

        request.session['wholesale_order'] = order_details

        if order_subtotal < 50:
            product_errors.append('Order sub total less than £50 minimum')

        if len(product_errors) == 0:
            url = '/wholesale_order/'
            if special is not None:
                url += special_name + '/'
            url += 'summary'
            return redirect(url)

    ctx = {
        'display_vat_message': display_vat_message,
        'display_brexit_message': display_brexit_message,
        'form': form,
        'postage_option': postage_option,
        'categories_products': categories_products,
        'create_order': create_order,
        'product_errors': product_errors,
        'subtotal': order_subtotal
    }

    return render(request, 'products.html', ctx)


def send_emails(ctx):

    subject = 'Painting Dreams Wholesale Order'
    headers = ("Content-Type: text/plain; charset = \"UTF-8\";\n"
               "Content-Transfer-Encoding: 8bit")

    shop_details = ('Shop name: ' + ctx['shop']['name'] + "\r\n"
                    'Shop address: ' + ctx['shop']['address'] + "\r\n")

    contact_details = ('Contact name: ' + ctx['contact']['name'] + "\r\n"
                       'Contact email: ' + ctx['contact']['email'] + "\r\n"
                       'Contact tel: ' + ctx['contact']['tel'])

    product_details = ''

    for product in ctx['products']:
        product_details += product['code'] + ' - '
        product_details += product['title'] + ' - '
        product_details += '£' + str(product['price']) + ' x ' + str(product['quantity']) + ': '
        product_details += '£' + str(product['total']) + "\r\n"

    product_details += "\r\n"

    if ctx['postage_option'] == 'std':
        product_details += ('Sub total: £' + str(ctx['order_sub_total']) + "\r\n"
                            'Delivery charge: £' + str(ctx['delivery_charge']) + "\r\n")

    product_details += 'Order total: £' + str(ctx['order_total']) + "\r\n\r\n"

    if ctx['postage_option'] == 'wghtcalc':
        product_details += "Carriage cost will be calculated depending on weight and you will be notified of the total cost before dispatch. Please confirm you are happy to proceed with the order once you have received the notification.\r\n\r\n";

    # Administrator email
    email_body =  "The following wholesale order has been placed.\r\n\r\n"
    email_body += shop_details + "\r\n"
    email_body += contact_details + "\r\n\r\n"
    email_body += product_details

    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, settings.WHOLESALE_ADMIN_EMAILS)

    mail_admins(subject, message=email_body)

    # Customer email
    email_body =  'Dear ' + ctx['contact']['name'] + ",\r\n\r\n"
    email_body += "Thank you for placing a wholesale order. This email shows the details you entered for your records.\r\n\r\n"
    email_body += shop_details + "\r\n"
    email_body += contact_details + "\r\n\r\n"
    email_body += product_details

    # Sanitise entered email
    customer_email = ctx['contact']['email'].replace("\r", '').replace("\n", '')

    send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [customer_email])


def store_order(ctx):
    order = Order.objects.create(
        shop_name = ctx['shop']['name'],
        shop_address = ctx['shop']['address'],
        contact_name = ctx['contact']['name'],
        contact_email = ctx['contact']['email'],
        contact_tel = ctx['contact']['tel'],
        special_name = ctx['special_name'],
        postage_option = ctx['postage_option'])
    # order.save()

    for product in ctx['products']:
        OrderLine.objects.create(
            order = order,
            code = product['code'],
            title = product['title'],
            item_price = product['price'],
            quantity = product['quantity']
        )
        # line.save()


def build_order(request, special_name='', complete=False):
    postage_option = 'none'
    special = None
    display_vat_message = True
    display_brexit_message = False

    if len(special_name) > 0:
        try:
            special = Special.objects.get(name=special_name)
            postage_option = special.postage_option
            display_vat_message = special.display_vat_message
            display_brexit_message = special.display_brexit_message
        except Special.DoesNotExist:
            raise Http404("Special form %s does not exist" % (special_name,))

    try:
        order_details = request.session['wholesale_order']

        categories_products = get_categories_products([])

        ctx = {
            'display_vat_message': display_vat_message,
            'display_brexit_message': display_brexit_message,
            'shop': {
                'name': order_details['shop_name'],
                'address': order_details['shop_address']
            },
            'contact': {
                'name': order_details['contact_name'],
                'email': order_details['contact_email'],
                'tel': order_details['contact_tel']
            },
            'products': [],
            'special_name': special_name,
            'special_name_len': len(special_name),
            'postage_option': postage_option
        }

        order_total = 0

        for cat_products in categories_products.values():
            for product in cat_products:
                if product.sold_out:
                    continue
                key = 'quantity_' + product.code
                if key in order_details:
                    product_total = product.price * order_details[key]
                    product = {
                        'code': product.code,
                        'title': product.title,
                        'price': product.price,
                        'quantity': order_details[key],
                        'total': product_total
                    }
                    order_total += product_total
                    ctx['products'].append(product)

        ctx['order_sub_total'] = order_total

        ctx['delivery_charge'] = 0
        if postage_option == 'std' and order_total < 100:
            ctx['delivery_charge'] = 8
            order_total += 8

        ctx['order_total'] = order_total

        if complete:
            send_emails(ctx)
            store_order(ctx)
            ctx['complete'] = True
            del request.session['wholesale_order']

        return render(request, 'summary.html', ctx)

    except KeyError:
        url = '/wholesale_order/'

        if special is not None:
            url += special_name

        return redirect(url)


def summary(request, special_name=''):
    return build_order(request, special_name)


def place_order(request, special_name=''):
    return build_order(request, special_name, complete=True)
