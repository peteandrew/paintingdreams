from mainapp.models import Image, Order, OrderLine, OrderAddress, OrderTransaction
from rest_framework import serializers

from django.urls import reverse
from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm
from mainapp.PayPalFormNiceRenderer import PayPalFormNiceRenderer

from cardsave.forms import CardsavePaymentForm

import logging
logger = logging.getLogger('django')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'slug', 'title', 'description', 'created', 'updated', 'products', 'tags')


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ('product', 'title', 'item_price', 'item_weight', 'quantity', 'line_price', 'line_weight', 'discounted')


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddress
        fields = ('address1', 'address2', 'address3', 'address4', 'city', 'state', 'post_code', 'country')


class OrderTransactionSerializer(serializers.ModelSerializer):
    form = serializers.SerializerMethodField()

    def get_form(self, obj):
        # logger.debug(obj.order.__dict__)

        if obj.payment_processor == 'paypal':
            paypal_dict = {
                "business": settings.PAYPAL_RECEIVER_EMAIL,
                "amount": obj.order.total_price,
                "currency_code": settings.PAYPAL_CURRENCY_CODE,
                "item_name": "Painting Dreams products",
                "invoice": obj.unique_id,
                "notify_url": settings.BASE_URL + reverse('paypal-ipn'),
                "return": settings.BASE_URL + reverse('order-transaction-complete'),
                "cancel_return": settings.BASE_URL + reverse('paypal-cancel')
            }
            paypal_form = PayPalPaymentsForm(initial=paypal_dict)
            payment_form = PayPalFormNiceRenderer(paypal_form)

        else:
            cardsave_dict = {
                "Amount": int(obj.order.total_price * 100), # Amount need to be in minor currency (i.e. pence for pound)
                "OrderID": obj.unique_id,
                "OrderDescription": "Painting Dreams products",
                "CustomerName": obj.order.customer_name,
                "Address1": obj.order.billing_address.address1,
                "Address2": obj.order.billing_address.address2,
                "Address3": obj.order.billing_address.address3,
                "Address4": obj.order.billing_address.address4,
                "City": obj.order.billing_address.city,
                "State": obj.order.billing_address.state,
                "PostCode": obj.order.billing_address.post_code,
                "CountryCode": obj.order.billing_address.country.numeric,
                "EmailAddress": obj.order.customer_email,
                "ServerResultURL": settings.BASE_URL + reverse('cardsave-result'),
                "CallbackURL": settings.BASE_URL + reverse('order-transaction-complete')
            }
            payment_form = CardsavePaymentForm(initial=cardsave_dict)

        return payment_form.render()

    class Meta:
        model = OrderTransaction
        fields = ('unique_id','payment_processor','state','created','updated','form','order')


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(source='orderline_set', many=True)
    order_transactions = OrderTransactionSerializer(source='ordertransaction_set', many=True, read_only=True)
    billing_address = OrderAddressSerializer()
    shipping_address = OrderAddressSerializer(required=False)

    class Meta:
        model = Order

        fields = (  'unique_id',
                    'customer_name',
                    'customer_email',
                    'billing_address',
                    'shipping_name',
                    'shipping_address',
                    'order_lines',
                    'sub_total_price',
                    'postage_price',
                    'total_price',
                    'order_transactions',
                    'state',
                    'discount_code',
                    'created',
                    'updated')

    def create(self, validated_data):
        order_lines = validated_data.pop('orderline_set')

        billing_address_data = validated_data.pop('billing_address')
        billing_address = OrderAddress.objects.create(**billing_address_data)

        try:
            shipping_address_data = validated_data.pop('shipping_address')
            shipping_address = OrderAddress.objects.create(**shipping_address_data)
        except KeyError:
            shipping_address = None

        order = Order.objects.create(billing_address=billing_address, shipping_address=shipping_address, **validated_data)

        for order_line in order_lines:
            OrderLine.objects.create(order=order, **order_line)

        return order
