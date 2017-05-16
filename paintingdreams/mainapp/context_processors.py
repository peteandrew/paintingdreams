import datetime
import pytz

from carton.cart import Cart
from mainapp.models import HolidayMessage

import logging
logger = logging.getLogger('django')


def basket(request):
    cart = Cart(request.session)
    return {'basket': cart}


def holiday_messages(request):
    message_objects = HolidayMessage.objects.filter(start__lte=datetime.datetime.now(tz=pytz.utc)).filter(end__gt=datetime.datetime.now(tz=pytz.utc))

    messages = {}
    for message_object in message_objects:
        if message_object.website_message:
            messages['website'] = message_object.website_message
        if message_object.email_message:
            messages['email'] = message_object.email_message
        if message_object.wholesale_message:
            messages['wholesale'] = message_object.wholesale_message

    logger.debug(messages)

    return {'holiday_messages': messages}
