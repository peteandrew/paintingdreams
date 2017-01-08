import time
import datetime

from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from cardsave.forms import CardsaveResultForm
from cardsave.models import PaymentResult
from cardsave import cardsave_hash
from cardsave.signals import payment_successful, payment_unsuccessful


def get_order_model():
    package, module = settings.CARDSAVE_ORDER_MODEL.rsplit('.', 1)
    return getattr(import_module(package), module)


def cardsave_response(status_code, message):
    response = HttpResponse('StatusCode=' + str(status_code) + '&Message=' + message)
    return response


@require_POST
@csrf_exempt
def cardsave_result(request):
    form = CardsaveResultForm(request.POST)

    if not form.is_valid():
        return cardsave_response(30, 'Unable to process Cardsave result. Invalid request')

    # Check order exists
    order_model = get_order_model()
    try:        
        order = order_model.objects.get(unique_id=form.cleaned_data['OrderID'])
    except:
        return cardsave_response(30, 'Unable to process Cardsave result. Order does not exist')

    # Check hashes matches
    vals = form.cleaned_data
    vals['Amount'] = int(order.total_price * 100)
    correct_result_hash = cardsave_hash.result_hash(vals)
    if form.cleaned_data['HashDigest'] != correct_result_hash:
        return cardsave_response(30, 'Unable to process Cardsave result. Hashes do not match')

    payment_result = PaymentResult(
        status_code = form.cleaned_data['StatusCode'],
        message = form.cleaned_data['Message'],
        previous_status_code = form.cleaned_data['PreviousStatusCode'],
        previous_message = form.cleaned_data['PreviousMessage'],
        cross_reference = form.cleaned_data['CrossReference'],
        order_id = form.cleaned_data['OrderID'],
        transaction_type = form.cleaned_data['TransactionType'],
        transaction_datetime = datetime.datetime.fromtimestamp(time.mktime(
            time.strptime(form.cleaned_data['TransactionDateTime'],
                          '%Y-%m-%d %H:%M:%S +00:00')), datetime.timezone.utc)
    )
    payment_result.save()

    # Send signals
    if form.cleaned_data['StatusCode'] != 0:
        payment_unsuccessful.send(sender=payment_result)
    else:
        payment_successful.send(sender=payment_result)

    return cardsave_response(0, '')
