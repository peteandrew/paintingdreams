from carton.cart import Cart
from mainapp.holiday_messages import messages

import logging
logger = logging.getLogger('django')


def basket(request):
    cart = Cart(request.session)
    return {'basket': cart}


def holiday_messages(request):
    return {'holiday_messages': messages()}
