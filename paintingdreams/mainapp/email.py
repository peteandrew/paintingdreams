import datetime
import pytz

from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from mainapp.models import HolidayMessage


def send_order_complete_email(order):
    message_objects = HolidayMessage.objects.filter(start__lte=datetime.datetime.now(tz=pytz.utc)).filter(end__gt=datetime.datetime.now(tz=pytz.utc))
    holiday_message = None
    for message_object in message_objects:
        if message_object.email_message:
            holiday_message = message_object.email_message

    msg_plain_admin = render_to_string('email/transaction-complete-admin.txt', {'order': order})
    msg_html_admin = render_to_string('email/transaction-complete-admin.html', {'order': order})
    msg_plain_customer = render_to_string('email/transaction-complete-customer.txt', {'order': order, 'holiday_message': holiday_message})
    msg_html_customer = render_to_string('email/transaction-complete-customer.html', {'order': order, 'holiday_message': holiday_message})

    # Mail site orders administrator
    mail.send_mail(
        subject='Order received',
        message=msg_plain_admin,
        from_email=settings.ORDERS_FROM_EMAIL,
        recipient_list=[settings.ORDERS_ADMIN_EMAIL],
        html_message=msg_html_admin)

    mail.mail_admins(
        subject='Order received',
        message=msg_plain_admin,
        html_message=msg_html_admin)

    # Mail customer
    mail.send_mail(
        subject='Painting Dreams Order',
        message=msg_plain_customer,
        from_email=settings.ORDERS_FROM_EMAIL,
        recipient_list=[order.customer_email],
        html_message=msg_html_customer)

    mail.mail_admins(
        subject='Painting Dreams Order',
        message=msg_plain_customer,
        html_message=msg_html_customer)


def send_payment_failed_email(order):
    msg_plain_customer = render_to_string('email/transaction-failed-customer.txt', {'order': order, 'site_base_url': settings.BASE_URL})
    msg_html_customer = render_to_string('email/transaction-failed-customer.html', {'order': order, 'site_base_url': settings.BASE_URL})

    # Mail customer
    mail.send_mail(
        subject='Painting Dreams Order Payment Failed',
        message=msg_plain_customer,
        from_email=settings.ORDERS_FROM_EMAIL,
        recipient_list=[order.customer_email],
        html_message=msg_html_customer)

    mail.mail_admins(
        subject='Painting Dreams Order Payment Failed',
        message=msg_plain_customer,
        html_message=msg_html_customer)
