from carton.cart import Cart

import logging
logger = logging.getLogger('django')

def basket(request):
    cart = Cart(request.session)
    return {'basket': cart}
