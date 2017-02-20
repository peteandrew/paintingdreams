from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string


def send_order_complete_email(order):
    msg_plain_admin = render_to_string('email/transaction-complete-admin.txt', {'order': order})
    msg_plain_customer = render_to_string('email/transaction-complete-customer.txt', {'order': order})
    #msg_html = render_to_string('templates/email.html', {'some_params': some_params})

    # Mail site orders administrator
    mail.send_mail(
        'Order received',
        msg_plain_admin,
        settings.ORDERS_FROM_EMAIL,
        [settings.ORDERS_ADMIN_EMAIL])

    # Mail customer
    mail.send_mail(
        'Painting Dreams Order',
        msg_plain_customer,
        settings.ORDERS_FROM_EMAIL,
        [order.customer_email])


def send_payment_failed_email(order):
    msg_plain_customer = render_to_string('email/transaction-failed-customer.txt', {'order': order, 'site_base_url': settings.BASE_URL})

    # Mail customer
    mail.send_mail(
        'Painting Dreams Order Payment Failed',
        msg_plain_customer,
        settings.ORDERS_FROM_EMAIL,
        [order.customer_email])
