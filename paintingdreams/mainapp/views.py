import os

from uuid import uuid4

from PIL import Image as PILImage, ImageDraw, ImageFont

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, Http404, QueryDict
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail

import logging

from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request as APIRequest
from rest_framework.response import Response as APIResponse
from rest_framework import status as APIStatus
from rest_framework.parsers import JSONParser, FormParser

from carton.cart import Cart

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

import cardsave.signals

from mainapp.models import Image, Product, ProductType, Order, OrderAddress, OrderLine, OrderTransaction, ImageWebimage, ImageTag, ImageImageTag
from mainapp.forms import OrderDetailsForm
from mainapp.email import send_order_complete_email, send_payment_failed_email
from mainapp import postage_prices
from mainapp import destination_classification
from mainapp.serializers import ImageSerializer, OrderSerializer, OrderTransactionSerializer

logger = logging.getLogger('django')


def session_order(request):
    return HttpResponse(request.session.get('order_id'))


def home(request):
    homepage_images = Image.objects.filter(tags__slug__exact='home')
    homepage_products = Product.objects.filter(tags__slug__exact='home')
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


def image_index(request, slug):
    base_imagetag = get_object_or_404(ImageTag, slug=slug)
    images = Image.objects.prefetch_related('webimages').filter(tags=base_imagetag)
    num_images = len(images)
    imagetag_images = [{'tag': base_imagetag, 'images': images}]

    child_imagetags_levels = base_imagetag.children()
    for level in child_imagetags_levels.keys():
        for tag in child_imagetags_levels[level]:
            images = Image.objects.prefetch_related('webimages').filter(tags=tag)
            num_images += len(images)
            imagetag_images.append({'tag': tag, 'images': images})

    pagetitle = base_imagetag.name
    context = {'imagetagimages': imagetag_images, 'numimages': num_images, 'pagetitle': pagetitle}

    if 1 in child_imagetags_levels:
        context['firstgenimagetags'] = child_imagetags_levels[1]

    return render(request, 'image/index.html', context)


def image_detail(request, slug):
    image = get_object_or_404(Image, slug=slug)
    products = Product.objects.filter(image=image)
    context = {'image': image, 'products': products, 'pagetitle': image.title}
    return render(request, 'image/detail.html', context)


def product_index(request, slug):
    base_product_type = get_object_or_404(ProductType, slug=slug)

    product_type_levels_ids = [(0, base_product_type.id,)] + base_product_type.child_ids()
    first_generation = []
    product_type_ids = []
    for product_type_level_id in product_type_levels_ids:
        if product_type_level_id[0] == 1:
            first_generation.append(product_type_level_id[1])
        product_type_ids.append(product_type_level_id[1])
    first_generation_product_types = ProductType.objects.filter(pk__in=first_generation)

    products = Product.objects.prefetch_related('product_type').select_related('image').prefetch_related('image__webimages').prefetch_related('webimages').filter(product_type_id__in=product_type_ids)

    pagetitle = base_product_type.displayname_final + 's'
    context = {'product_type': base_product_type, 'products': products, 'pagetitle': pagetitle, 'first_generation_product_types': first_generation_product_types}

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

    context = {'product': product, 'pagetitle': pagetitle}
    return render(request, 'product/detail.html', context)


def search(request):
    api_request = APIRequest(request)
    response = api_search(api_request)

    ctx = response.data
    ctx['query'] = request.GET.get('query', '')
    return render(request, 'search.html', ctx)


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
    cart.set_quantity(product, quantity=request.POST['quantity'])

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
    # Calculate order total weight and shipping price
    weight = 0
    for item in items:
        item_weight = item.product.product_type.shipping_weight_final
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


def order_start(request):
    cart = Cart(request.session)
    if len(cart.items) < 1:
        return redirect('/')

    if request.method == 'POST':
        form = OrderDetailsForm(request.POST)
        if form.is_valid():
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
                'billing_address2': details['billing_address']['address2'],
                'billing_address3': details['billing_address']['address3'],
                'billing_address4': details['billing_address']['address4'],
                'billing_city': details['billing_address']['city'],
                'billing_state': details['billing_address']['state'],
                'billing_post_code': details['billing_address']['post_code'],
                'billing_country': details['billing_address']['country']
            }

            if 'shipping_address' in details and details['shipping_address'] is not None:
                form_vals.update({
                    'shipping_name': details['shipping_name'],
                    'shipping_address1': details['shipping_address']['address1'],
                    'shipping_address2': details['shipping_address']['address2'],
                    'shipping_address3': details['shipping_address']['address3'],
                    'shipping_address4': details['shipping_address']['address4'],
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

    ctx = {
        'order': order
    }

    order_transaction_list_view = OrderTransactionListView()
    get_current_transaction = False

    if request.method == 'POST':
        # Cancel current transaction if there is one and user has chosen to cancel it
        if order.current_transaction:
            if request.POST.get('cancel-current-trans', False):
                trans = order.current_transaction
                trans.state = 'cancelled'
                trans.save()
            else:
                get_current_transaction = True
        else:
            api_request = APIRequest(request, (FormParser(),))
            response = order_transaction_list_view.post(api_request, order_id)
            # if response.status_code == 204:
            ctx['transaction'] = response.data
    else:
        get_current_transaction = True

    if get_current_transaction:
        get_copy = request.GET.copy()
        get_copy['current'] = 'true'
        request.GET = get_copy
        api_request = APIRequest(request)
        response = order_transaction_list_view.get(api_request, order_id)
        if response.status_code == 200:
            ctx['transaction'] = response.data

    # Need to output most recent current transactions in template with prompt to
    # change payment method. In change payment method box need to display warning not
    # to change method if already successfully submitted payment.

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

    ctx = {
        'order': order
    }

    return render(request, 'order/complete.html', ctx)


def order_transaction_complete_test(request):
    order_address = OrderAddress(address1='test address', address2='test line 2', city='blah', country='GB')
    order_address.save()
    order = Order(customer_name='test', customer_email='test@example.com', billing_address=order_address, shipping_address=order_address, postage_price=3.50,)
    order.save()
    product1 = Product.objects.all()[0]
    product2 = Product.objects.all()[1]
    orderline = OrderLine(product=product1, title='Product 1', item_price=25.50, item_weight=150, quantity=3, order=order)
    orderline.save()
    orderline = OrderLine(product=product2, title='Product 2', item_price=55.50, item_weight=550, quantity=2, order=order)
    orderline.save()
    order_transaction = OrderTransaction(order=order, payment_processor='cardsave')
    order_transaction.state = request.GET.get('state', 'started')
    order_transaction.save()
    if order_transaction.state == 'complete':
        order.state = 'paid'
        order.save()
    ctx = {
        'order': order
    }
    return render(request, 'order/complete.html', ctx)


def temp_complete_order_transaction(request):
    transaction = OrderTransaction.objects.get(unique_id=request.GET['id'])

    # Update transaction state
    transaction.state = 'complete'
    transaction.save()

    # Update order state
    transaction.order.state = 'paid'
    transaction.order.save()

    # Send emails
    send_order_complete_email(transaction.order)

    return HttpResponse('Set paid')


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

    if sender.mc_gross != transaction.order.total_price:
        # PayPal amount doesn't match order amount. Fail
        logger.debug('paypal_ipn_handler: Error mc_gross did not match order total')
        logger.debug(sender.__dict__)
        return

    # Update transaction state
    transaction.state = 'complete'
    transaction.save()

    # Update order state
    transaction.order.state = 'paid'
    transaction.order.save()

    # Send emails
    send_order_complete_email(transaction.order)


@csrf_exempt
def paypal_cancel(request):
    # Check that we have a valid order in the session. Redirect to home page
    # if we don't
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('/')

    try:
        order = Order.objects.get(unique_id=order_id)
    except:
        return redirect('/')

    if order.last_transaction.payment_processor != 'paypal':
        return redirect('/')

    transaction = order.last_transaction
    transaction.state = 'cancelled'
    transaction.save()

    return redirect('/order-complete')


@receiver(cardsave.signals.payment_successful)
def cardsave_payment_successful_handler(sender, **kwargs):
    try:
        transaction = OrderTransaction.objects.get(unique_id=sender.order_id)
    except:
        # This shouldn't happen as transaction is checked in Cardsave callback. Fail.
        return

    # Update order transaction state
    transaction.state = 'complete'
    transaction.save()
    # Update order state
    transaction.order.state = 'paid'
    transaction.order.save()

    # Send emails
    send_order_complete_email(transaction.order)


@receiver(cardsave.signals.payment_unsuccessful)
def cardsave_payment_unsuccessful_handler(sender, **kwargs):
    try:
        transaction = OrderTransaction.objects.get(unique_id=sender.order_id)
    except:
        # This shouldn't happen as transaction is checked in Cardsave callback. Fail.
        return

    # Update order transaction state
    transaction.state = 'failed'
    transaction.save()

    # Send emails
    send_payment_failed_email(transaction.order)


def mailtest(request):
    logger.debug(request.__dict__)
    #send_mail('test mail', 'A test email', settings.DEFAULT_FROM_EMAIL, ['peteandrew101@gmail.com'])


class ImageListView(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def __get_address_dict(self, prefix, data):
        address_keys = ['address1','address2','address3','address4','city', 'state', 'post_code', 'country']
        address = {}
        for key in address_keys:
            data_key = prefix + '_' + key
            try:
                address[key] = data[data_key]
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
                "item_weight": cart_item.product.product_type.shipping_weight_final,
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
    product_match = {
        'title': product.displayname,
        'thumbnail': product.webimages.first().filename()
    }
    if product.image:
        product_match['slug'] = product.image.slug + '__' + product.product_type.slug
    else:
        product_match['slug'] = product.product_type.slug

    if product.displayname.lower() == query.lower():
        product_exact_match = product_match
    else:
        product_matches.append(product_match)

    return product_exact_match, product_matches


def add_image_match(query, image, image_exact_match, image_matches):
    image_match = {
        'title': str(image),
        'thumbnail': image.webimages.first().filename(),
        'slug': image.slug
    }

    if str(image).lower() == query.lower():
        image_exact_match = image_match
    else:
        image_matches.append(image_match)

    return image_exact_match, image_matches


@api_view()
def api_search(request):
    query = request.query_params.get('query')
    if not query:
        return APIResponse({"error": "No search query"})

    query = query.replace('-','')
    query_words = query.split(' ')
    products_word_matches = {}
    for product in Product.objects.all():
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


    query_words = query.split(' ')
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

    # for product in Product.objects.filter(tags__name__icontains=query):
        # product_tag_list.append(product.displayname)
    # for image in Image.objects.filter(tags__name__icontains=query):
        # image_tag_list.append(str(image))

    return APIResponse({
        "product_exact_match": product_exact_match,
        "product_matches": product_matches,
        "image_exact_match": image_exact_match,
        "image_matches": image_matches})
