from django.db.models import Q

from mainapp.models import PostagePrice


def calculate(destination, weight):
    prices = PostagePrice.objects.filter(
        destination = destination,
        min_weight__lte = weight).filter(
            Q(max_weight__exact = None) | Q(max_weight__gte = weight))

    if len(prices) > 0:
        return prices[0].price
    else:
        return 0
