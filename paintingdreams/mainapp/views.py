import os
import json
import re

import requests

from datetime import datetime, timedelta, timezone

from uuid import uuid4

from PIL import Image as PILImage, ImageDraw, ImageFont

from django.db.models import F
from django.db import IntegrityError, transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, Http404, QueryDict
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required

import logging

from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request as APIRequest
from rest_framework.response import Response as APIResponse
from rest_framework import status as APIStatus
from rest_framework.parsers import JSONParser, FormParser

from itertools import chain

from carton.cart import Cart

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

import cardsave.signals

from mainapp.models import (
    Image,
    ImageTag,
    Product,
    ProductType,
    ProductTag,
    Order,
    OrderAddress,
    OrderLine,
    OrderTransaction,
    ImageWebimage,
    Gallery,
    ImageGallery,
    HomePageWebimage,
    ProductTypeAdditionalProduct,
    ProductAdditionalProduct,
    FestivalPage,
)
from mainapp.forms import OrderDetailsForm, MailingListSubscribeForm
from mainapp.email import send_order_complete_email, send_payment_failed_email
from mainapp import postage_prices
from mainapp import destination_classification
from mainapp.serializers import ImageSerializer, OrderSerializer, OrderTransactionSerializer
from mainapp.recaptcha import check_recaptcha
from mainapp.mailchimp import mailchimp_subscribe

logger = logging.getLogger('django')


def home(request):
    homepage_images = HomePageWebimage.objects.filter(enabled=True).order_by('order')
    homepage_products = Product.objects.filter(
        tags__slug__exact='home'
    ).filter(
        sold_out=False
    ).filter(
        temporarily_unavailable=False
    ).order_by('-updated')
    context = {'homepage_images': homepage_images, 'homepage_products': homepage_products}
    return render(request, 'home.html', context)


def original_file_serve(request, filename):
    if request.user.is_superuser:
        response = HttpResponse()
        url = '/media/images/original/' + filename
        response['Content-Type'] = ''
        length = os.path.getsize(settings.MEDIA_ROOT + '/images/original/' + filename)
        response['Content-Length'] = str(length)
        response['X-Accel-Redirect'] = url
        return response
    else:
        return HttpResponseForbidden('Restricted Access')


def artist_info(request):
    ctx = {'pagetitle': 'Artist info'}
    return render(request, 'artist_info.html', ctx)


def shows(request):
    ctx = {'pagetitle': 'Shows'}
    return render(request, 'shows.html', ctx)


def feedback(request):
    ctx = {'pagetitle': 'Customer feedback'}
    return render(request, 'feedback.html', ctx)


def wholesale_info(request):
    ctx = {'pagetitle': 'Wholesale info'}
    return render(request, 'wholesale_info.html', ctx)


def delivery_info(request):
    ctx = {'pagetitle': 'Delivery info'}
    return render(request, 'delivery_info.html', ctx)


def terms_and_conditions(request):
    ctx = {'pagetitle': 'Terms and Conditions'}
    return render(request, 'terms_and_conditions.html', ctx)


def gallery(request, slug):
    base_gallery = get_object_or_404(Gallery, slug=slug)
    images = Image.objects.prefetch_related('webimages').filter(galleries=base_gallery).order_by('imagegallery__order')
    num_images = len(images)
    gallery_images = [{'gallery': base_gallery, 'images': images}]

    gallery_children = base_gallery.children()
    for child in gallery_children:
        images = Image.objects.prefetch_related('webimages').filter(galleries__in=child['branch_ids']).order_by('galleries__gallery__order', 'galleries')
        if len(images) == 0:
            continue
        num_images += len(images)
        gallery_images.append({'gallery': child['gallery'], 'images': images})

    pagetitle = base_gallery.name
    context = {'gallery_images': gallery_images, 'num_images': num_images, 'pagetitle': pagetitle}

    return render(request, 'image/gallery.html', context)


def image_detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    products = Product.objects.filter(image=image, hidden=False)

    max_image_height = 0
    for webimage in image.webimages.all():
        sizes = json.loads(webimage.sizes)
        if sizes['standard'][1] > max_image_height:
            max_image_height = sizes['standard'][1]

    context = {'image': image, 'products': products, 'pagetitle': image.title, 'max_image_height': max_image_height}
    return render(request, 'image/detail.html', context)


def product_index(request, slug):
    base_product_type = get_object_or_404(ProductType, slug=slug)
    products = list(Product.objects.prefetch_related('product_type').select_related('image').prefetch_related('image__webimages').prefetch_related('webimages').filter(product_type=base_product_type).filter(hidden=False).order_by('product_type_order'))
    num_products = len(products)
    additional_products = ProductTypeAdditionalProduct.objects.select_related('product__image').prefetch_related('product__image__webimages').prefetch_related('product__webimages').filter(product_type=base_product_type).filter(product__hidden=False)
    num_products += len(additional_products)
    for product in additional_products:
        products.append(product.product)
    producttype_products = [{'producttype': base_product_type, 'products': products}]
    disp_categories = False

    product_type_children = base_product_type.children()
    for child in product_type_children:
        if not child['product_type'].subproduct_hide:
            disp_categories = True
        products = Product.objects.prefetch_related('product_type').select_related('image').prefetch_related('image__webimages').prefetch_related('webimages').filter(product_type_id__in=child['branch_ids']).filter(hidden=False).order_by('product_type__order', 'product_type_order')
        if len(products) == 0:
            continue
        num_products += len(products)
        producttype_products.append({'producttype': child['product_type'], 'products': products})

    pagetitle = base_product_type.title + 's'
    context = {'product_type_products': producttype_products, 'num_products': num_products, 'pagetitle': pagetitle, 'listing_message': base_product_type.product_listing_message, 'index_inline': base_product_type.index_inline, 'disp_categories': disp_categories}

    return render(request, 'product/index.html', context)


def product_detail(request, slug):
    slug_components = slug.split('__')

    if len(slug_components) == 1:
        product_type = get_object_or_404(ProductType, slug=slug_components[0])
        if not product_type.stand_alone_final:
            raise Http404('Detail page does not exist for product')
        try:
            product = Product.objects.filter(product_type=product_type)[0]
        except IndexError:
            raise Http404('Detail page does not exist for product')

    else:
        image = get_object_or_404(Image, slug=slug_components[0])
        product_type = get_object_or_404(ProductType, slug=slug_components[1])
        if product_type.stand_alone_final:
            raise Http404('Detail page does not exist for product')
        try:
            product = Product.objects.filter(product_type=product_type).filter(image=image)[0]
        except IndexError:
            raise Http404('Detail page does not exist for product')

    pagetitle = ''
    if product.image:
        pagetitle += product.image.title + ' '
    pagetitle += product.product_type.displayname_final

    max_image_height = 0
    for webimage in product.webimages.all():
        sizes = json.loads(webimage.sizes)
        if sizes['standard'][1] > max_image_height:
            max_image_height = sizes['standard'][1]

    product_additional_products = ProductAdditionalProduct.objects.filter(product=product)
    additional_products = [product_additional_product.additional_product for product_additional_product in product_additional_products]

    context = {'product': product, 'pagetitle': pagetitle, 'max_image_height': max_image_height, 'additional_products': additional_products}
    return render(request, 'product/detail.html', context)


def festival_page(request, slug):
    page = get_object_or_404(FestivalPage, slug=slug)
    page_content = page.details
    images = page.webimages.order_by('order').all()

    # group 0: entire placeholder
    # group 1: image index
    # group 2: size attribute
    # group 3: size
    image_placeholders = re.findall(r'(<div id="img(\d*)"( size="(\d*)")?></div>)', page_content)
    for placeholder_details in image_placeholders:
        image_idx = int(placeholder_details[1])
        if image_idx >= len(images):
            continue
        image = images[image_idx]

        if placeholder_details[3]:
            image_size = placeholder_details[3]
        else:
            image_size = 600

        page_content = page_content.replace(
            placeholder_details[0],
            (
                '<div class="festival-details-webimage">'
                f'<a href="/media/images/extra-large-no-watermark/{image.filename()}"><img src="/media/images/enlargement/{image.filename()}" alt="{image.name}" class="img-responsive center-block" width="{image_size}" /></a>'
                '<p class="enlargement-text"><i class="fa fa-search-plus" aria-hidden="true"></i> Click image for enlargement</p>'
                '</div>'
            ),
        )

    products = page.products.prefetch_related('webimages').order_by('festivalpageproduct__order')

    context = {
        'pagetitle': page.title,
        'page': page,
        'page_content': page_content,
        'products': products,
    }
    return render(request, 'festival/detail.html', context)


def search(request):
    response = api_search(request)

    ctx = response.data
    ctx['query'] = request.GET.get('query', '')
    ctx['pagetitle'] = 'Search results'
    return render(request, 'search.html', ctx)


@require_POST
def basket_add(request):
    product = Product.objects.get(pk=request.POST['product_id'])
    cart = Cart(request.session)
    cart.add(product, price=product.product_type.price_final, quantity=request.POST['quantity'])

    if request.is_ajax():
        return HttpResponse()

    else:
        return redirect('/basket')


def basket_change_quantity(request):
    product = Product.objects.get(pk=request.POST['product_id'])
    cart = Cart(request.session)
    try:
        quantity = int(request.POST['quantity'])
    except ValueError:
        quantity = 0
    cart.set_quantity(product, quantity=quantity)

    if request.is_ajax():
        return HttpResponse()

    else:
        return redirect('/basket')


def basket_change_destination(request):
    destination = request.POST['destination']
    if destination in ['GB','EUROPE','WORLD']:
        request.session['destination'] = destination

    return redirect('/basket')


def calc_postage(destination, items):

    # For each item, get product type with shipping weight and shipping weight multiple (with product type inherited from)
    # Find items where quantity is 1 and where product type for shipping weight multiple doesn't exist in any of the other items
    # For other items, use shipping weight multiple


    # Calculate order total weight and shipping price
    weight = 0
    for item in items:
        if item.quantity > 1:
            item_weight = item.product.product_type.shipping_weight_multiple_final(destination)
        else:
            item_weight = item.product.product_type.shipping_weight_final(destination)

        weight += item.quantity * item_weight

    price = postage_prices.calculate(destination, weight)

    return {'weight': weight, 'price': price}


def basket_show(request):
    cart = Cart(request.session)

    if not request.session.get('destination'):
        request.session['destination'] = 'GB'

    postage = calc_postage(request.session['destination'], cart.items)
    order_total = cart.total + postage['price']

    context = {
        'pagetitle': 'Shopping basket',
        'cart': cart,
        'weight': postage['weight'],
        'destination': request.session['destination'],
        'postage_price': postage['price'],
        'order_total': order_total
    }
    return render(request, 'basket/index.html', context)


def mailinglist_subscribe(request):
    if request.method != 'POST':
        form = MailingListSubscribeForm()
        return render(request, 'mailinglist_subscribe.html', {'form': form,})

    form = MailingListSubscribeForm(request.POST)
    ctx = {'form': form, 'subscribed': False}

    if not form.is_valid():
        return render(request, 'mailinglist_subscribe.html', ctx)

    if not check_recaptcha(request):
        form.add_error(None, 'Invalid reCAPTCHA. Please try again.')
    else:
        subscriber = form.cleaned_data
        if not mailchimp_subscribe(subscriber, 'signupform'):
            form.add_error(None, 'Sorry, an error occurred while subscribing you to the mailing list.')
        else:
            ctx['subscribed'] = True

    return render(request, 'mailinglist_subscribe.html', ctx)


def order_start(request):
    cart = Cart(request.session)
    if len(cart.items) < 1:
        return redirect('/')

    if request.method == 'POST':
        form = OrderDetailsForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if form_data['mailinglist_subscribe']:
                subscriber = {
                    'email': form_data['customer_email'],
                    'first_name': form_data['customer_name'].split(' ')[0],
                    'last_name': ' '.join(form_data['customer_name'].split(' ')[1:])
                }
                mailchimp_subscribe(subscriber, 'orderform')

            order_list_view = OrderListView()
            api_request = APIRequest(request, (FormParser(),))
            response = order_list_view.post(api_request)

            # Need to check response here and make sure we get a 201

            return redirect('/order-payment')

    else:
        details = None

        # Use cutomer details from session if they exist
        if request.session.get('customer_details'):
            details = request.session.get('customer_details')

        form_vals = None
        if details:
            form_vals = {
                'customer_name': details['customer_name'],
                'customer_email': details['customer_email'],
                'billing_address1': details['billing_address']['address1'],
                'billing_2sserdda': details['billing_address']['address2'],
                'billing_3sserdda': details['billing_address']['address3'],
                'billing_4sserdda': details['billing_address']['address4'],
                'billing_city': details['billing_address']['city'],
                'billing_state': details['billing_address']['state'],
                'billing_post_code': details['billing_address']['post_code'],
                'billing_country': details['billing_address']['country']
            }

            if 'shipping_address' in details and details['shipping_address'] is not None:
                form_vals.update({
                    'shipping_name': details['shipping_name'],
                    'shipping_address1': details['shipping_address']['address1'],
                    'shipping_2sserdda': details['shipping_address']['address2'],
                    'shipping_3sserdda': details['shipping_address']['address3'],
                    'shipping_4sserdda': details['shipping_address']['address4'],
                    'shipping_city': details['shipping_address']['city'],
                    'shipping_state': details['shipping_address']['state'],
                    'shipping_country': details['shipping_address']['country']
                })

        form = OrderDetailsForm(form_vals)

    ctx = {'form': form,}
    return render(request, 'order/start.html', ctx)


def order_payment(request):
    # Check if order is complete and if so redirect to complete page

    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('/')

    try:
        order = Order.objects.get(unique_id=order_id)
    except:
        return redirect('/')

    if order.shipping_address:
        country = order.shipping_address.country
    else:
        country = order.billing_address.country
    classification = destination_classification.classify(country)
    if classification in ('EUROPE', 'WORLD'):
        international = True
    else:
        international = False

    ctx = {
        'order': order,
        'international': international,
    }

    order_transaction_list_view = OrderTransactionListView()
    get_current_transaction = True

    if request.method == 'POST' and request.POST.get('payment_processor'):
        if not order.current_transaction:
            get_current_transaction = False
            api_request = APIRequest(request, (FormParser(),))
            response = order_transaction_list_view.post(api_request, order_id)
            # if response.status_code == 204:
            ctx['transaction'] = response.data

    # We have to get the transaction from the order transaction API in order to
    # to get the payment processor form
    if get_current_transaction:
        get_copy = request.GET.copy()
        get_copy['current'] = 'true'
        request.GET = get_copy
        api_request = APIRequest(request)
        response = order_transaction_list_view.get(api_request, order_id)
        if response.status_code == 200:
            ctx['transaction'] = response.data

    return render(request, 'order/payment_selection.html', ctx)


@csrf_exempt
def order_transaction_complete(request):
    # Check that we have a valid order in the session. Redirect to home page
    # if we don't
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('/')

    try:
        order = Order.objects.get(unique_id=order_id)
    except:
        return redirect('/')

    # Clear basket
    if order.state == 'paid':
        try:
            cart = Cart(request.session)
            cart.clear()
        except:
            pass

    if not order.shipping_name:
        order.shipping_name = order.customer_name

    if not order.shipping_address:
        order.shipping_address = order.billing_address

    ctx = {
        'order': order
    }

    return render(request, 'order/complete.html', ctx)


@permission_required('mainapp.change_product_stock_count', login_url='admin:login')
def product_stock_count_list(request):
    if request.method == 'POST':
        product = Product.objects.get(pk = request.POST.get('product_id'))
        if 'stock_count' in request.POST:
            product.stock_count = request.POST.get('stock_count')
            product.save()
        elif 'sold_out' in request.POST:
            if request.POST.get('sold_out') == 'true':
                product.sold_out = True
            else:
                product.sold_out = False
            product.save()

    products = Product.objects.exclude(hidden=True).all()
    products = sorted(products, key=lambda prod: prod.displayname)

    ctx = {
        'products': products
    }

    return render(request, 'product/stock_count_list.html', ctx)


@permission_required('mainapp.view_order', login_url='admin:login')
def orders_list(request):
    from_dt = datetime.now(tz=timezone.utc) - timedelta(days=7)
    orders = (
        Order.objects.filter(state='paid')
        .filter(updated__gte=from_dt)
        .select_related('billing_address')
        .select_related('shipping_address')
        .prefetch_related('ordertransaction_set')
        .prefetch_related('orderline_set')
        .order_by('-updated')
    )

    ctx = {
        'orders': orders
    }

    return render(request, 'order/order_list.html', ctx)


def _handle_order_transaction_success(order_transaction):
    # Update transaction state
    order_transaction.state = 'complete'
    order_transaction.save()

    # Update order state
    order_transaction.order.state = 'paid'
    order_transaction.order.save()

    # Adjust product stock counts
    for orderline in order_transaction.order.orderline_set.all():
        # Skip any orderlines without products
        if not orderline.product:
            continue
        orderline.product.stock_count = F('stock_count') - orderline.quantity
        try:
            with transaction.atomic():
                orderline.product.save()
        except IntegrityError:
            with transaction.atomic():
                orderline.product.stock_count = 0
                orderline.product.save()
        orderline.product.refresh_from_db()

        # Mark products with zero stock count as sold out
        if orderline.product.stock_count == 0:
            orderline.product.sold_out = True
            orderline.product.save()

    # Send emails
    send_order_complete_email(order_transaction.order)


def _handle_order_transaction_failed(transaction, message):
    # Update order transaction state
    transaction.state = 'failed'
    transaction.message = message
    transaction.save()

    # Send emails
    send_payment_failed_email(transaction.order)


@receiver(valid_ipn_received)
def paypal_ipn_handler(sender, **kwargs):
    logger.debug(sender.__dict__)

    if sender.payment_status != ST_PP_COMPLETED:
        return

    try:
        transaction = OrderTransaction.objects.get(unique_id=sender.invoice)
    except:
        # Something wrong with PayPal IPN or site DB. Fail
        logger.debug('paypal_ipn_handler: Error getting transaction')
        logger.debug(sender.__dict__)
        return

    # Need to check that sender.receiver_email == settings.PAYPAL_RECEIVER_EMAIL

    # Need to re-add this check
    #if sender.mc_gross != transaction.order.total_price:
    #    # PayPal amount doesn't match order amount. Fail
    #    logger.debug('paypal_ipn_handler: Error mc_gross did not match order total')
    #    logger.debug(sender.__dict__)
    #    return

    _handle_order_transaction_success(transaction)


@csrf_exempt
def paypal_cancel(request):
    return redirect('/')


@receiver(cardsave.signals.payment_successful)
def cardsave_payment_successful_handler(sender, **kwargs):
    logger.debug(sender.__dict__)

    try:
        transaction = OrderTransaction.objects.get(unique_id=sender.order_id)
    except:
        # This shouldn't happen as transaction is checked in Cardsave callback. Fail.
        return

    _handle_order_transaction_success(transaction)


@receiver(cardsave.signals.payment_unsuccessful)
def cardsave_payment_unsuccessful_handler(sender, **kwargs):
    logger.debug(sender.__dict__)

    try:
        transaction = OrderTransaction.objects.get(unique_id=sender.order_id)
    except:
        # This shouldn't happen as transaction is checked in Cardsave callback. Fail.
        return

    _handle_order_transaction_failed(transaction, sender.message)


class ImageListView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def __get_address_dict(self, prefix, data):
        address_keys = [
            ('address1','address1'),
            ('address2','2sserdda'),
            ('address3','3sserdda'),
            ('address4','4sserdda'),
            ('city','city'),
            ('state','state'),
            ('post_code','post_code'),
            ('country','country')
        ]
        address = {}
        for key in address_keys:
            data_key = prefix + '_' + key[1]
            try:
                address[key[0]] = data[data_key]
            except KeyError:
                pass

        # Check we have a valid address
        if 'address1' not in address or len(address['address1']) < 1 or 'country' not in address or len(address['country']) < 1:
            return None

        return address


    def get_queryset(self):
        # In future we might want to check whether user is admin and return all order if so
        # Or if normal user logged in return all of their previous orders
        # For now we'll just return the current order
        return Order.objects.filter(unique_id=self.request.session.get('order_id'))

    def create(self, request):
        cart = Cart(request.session)
        if len(cart.items) < 1:
            errors = {'errors': 'No items in basket'}
            return APIResponse(errors, status=APIStatus.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        if isinstance(data, QueryDict):
            data = data.dict()

        order_lines = []
        for cart_item in cart.items:
            order_lines.append({
                "product": cart_item.product.id,
                "title": cart_item.product.displayname,
                "item_price": cart_item.product.product_type.price_final,
                "item_weight": cart_item.product.product_type.shipping_weight_final(),
                "quantity": cart_item.quantity
            })

        # Need to allow for addresses as flat structure (as will be the case with form posted data)
        # and addresses as sub objects (as will be the case with JSON posted data)
        billing_address_dict = self.__get_address_dict('billing', data)
        if billing_address_dict:
            data['billing_address'] = billing_address_dict

        shipping_address_dict = self.__get_address_dict('shipping', data)
        if shipping_address_dict:
            data['shipping_address'] = shipping_address_dict

        try:
            address = data['shipping_address']
        except KeyError:
            address = data['billing_address']

        destination = destination_classification.classify(address['country'])
        postage = calc_postage(destination, cart.items)

        data['order_lines'] = order_lines
        data['postage_price'] = postage['price']

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            request.session['order_id'] = serializer.data['unique_id']

            customer_details = {
                'customer_name': serializer.data['customer_name'],
                'customer_email': serializer.data['customer_email'],
                'billing_address': serializer.data['billing_address']
            }
            if 'shipping_address' in serializer.data:
                customer_details['shipping_name'] = serializer.data['shipping_name']
                customer_details['shipping_address'] = serializer.data['shipping_address']
            request.session['customer_details'] = customer_details

            return APIResponse(serializer.data, status=APIStatus.HTTP_201_CREATED)

        return APIResponse(serializer.errors, status=APIStatus.HTTP_400_BAD_REQUEST)


class OrderTransactionListView(APIView):
    def __get_order(self, request, order_id):
        if order_id != request.session.get('order_id'):
            return APIResponse({}, APIStatus.HTTP_401_UNAUTHORIZED)

        try:
            order = Order.objects.get(unique_id=order_id)
        except:
            return APIResponse({}, APIStatus.HTTP_404_NOT_FOUND)

        return order


    def get(self, request, order_id, format=None):
        order = self.__get_order(request, order_id)
        if isinstance(order, APIResponse):
            return order

        if not request.query_params.get('current', False):
            transactions = order.ordertransaction_set.all()
            serializer = OrderTransactionSerializer(transactions, many=True)
        else:
            transaction = order.current_transaction
            if not transaction:
                return APIResponse({}, APIStatus.HTTP_404_NOT_FOUND)
            serializer = OrderTransactionSerializer(transaction)

        return APIResponse(serializer.data)


    def post(self, request, order_id, format=None):
        order = self.__get_order(request, order_id)
        if isinstance(order, APIResponse):
            return order

        if order.current_transaction:
            return APIResponse({'error': 'Current transaction exists'}, status=APIStatus.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['order'] = order_id

        serializer = OrderTransactionSerializer(data=data)
        if serializer.is_valid():
            trans = serializer.save()
            return APIResponse(serializer.data, status=APIStatus.HTTP_201_CREATED)

        return APIResponse(serializer.errors, status=APIStatus.HTTP_400_BAD_REQUEST)


def add_product_match(query, product, product_exact_match, product_matches):
    # Skip any products without webimages
    if product.webimages.count() == 0:
        return product_exact_match, product_matches

    product_match = {
        'title': product.displayname,
        'thumbnail': product.webimages.first().filename(),
        'slug': ''
    }

    if product.image:
        product_match['slug'] = product.image.slug + '__' + product.product_type.slug
    else:
        product_match['slug'] = product.product_type.slug

    if product.displayname.lower() == query.lower():
        product_exact_match = product_match
    else:
        if product_match not in product_matches:
            product_matches.append(product_match)

    return product_exact_match, product_matches


def add_image_match(query, image, image_exact_match, image_matches):
    # Skip any images without webimages
    if image.webimages.count() == 0:
        return image_exact_match, image_matches

    image_match = {
        'title': str(image),
        'thumbnail': image.webimages.first().filename(),
        'slug': image.slug
    }

    if str(image).lower() == query.lower():
        image_exact_match = image_match
    else:
        if image_match not in image_matches:
            image_matches.append(image_match)

    return image_exact_match, image_matches


@api_view()
def api_search(request):
    query = request.query_params.get('query')
    if not query:
        return APIResponse({"error": "No search query"})

    query = query.replace('-','').lower()

    if len(query) < 3:
        return APIResponse({"error": "Query too short"})

    query_words = query.split(' ')
    # Remove any empty words
    query_words = [word for word in query_words if len(word) > 0]

    products_word_matches = {}
    for product in Product.objects.all():
        if product.hidden:
            continue

        displayname = product.displayname
        words_matched = 0

        for word in query_words:
            search_word = word
            # Remove pluralization
            if search_word[-1] == 's':
                search_word = search_word[:-1]
            if displayname.lower().find(search_word) != -1:
                words_matched += 1

        if words_matched > 0:
            try:
                products_word_matches[words_matched].append(product)
            except KeyError:
                products_word_matches[words_matched] = [product]

    product_exact_match = None
    product_matches = []
    for key in sorted(list(products_word_matches.keys()), reverse=True):
        # If there are more than one query words, skip products with only one matched words
        if key == 1 and len(query_words) > 1:
            continue

        for product in products_word_matches[key]:
            product_exact_match, product_matches = add_product_match(query, product, product_exact_match, product_matches)

    remove_words = []
    images = Image.objects
    for word in query_words:
        test_images = images.filter(title__icontains=word)
        if len(test_images) > 0:
            remove_words.append(word)
            images = test_images

    if len(remove_words) == 0:
        images = []

    image_exact_match = None
    image_matches = []
    for image in images:
        image_exact_match, image_matches = add_image_match(query, image, image_exact_match, image_matches)

    for product in Product.objects.filter(tags__in=ProductTag.objects.filter(name__icontains=query)):
        _, product_matches = add_product_match(query, product, None, product_matches)

    for image in Image.objects.filter(galleries__in=Gallery.objects.filter(name__icontains=query)):
        _, image_matches = add_image_match(query, image, None, image_matches)

    for image in Image.objects.filter(tags__in=ImageTag.objects.filter(name__icontains=query)):
        _, image_matches = add_image_match(query, image, None, image_matches)

    return APIResponse({
        "product_exact_match": product_exact_match,
        "product_matches": product_matches,
        "image_exact_match": image_exact_match,
        "image_matches": image_matches})
