from decimal import Decimal

from django.conf import settings

from mainapp.models import Product

SESSION_KEY = 'CART'


class CartItem:
    """
    A cart item, with the associated product, its quantity and its price.
    """
    def __init__(self, product, quantity, price, discounted, original_price):
        self.product = product
        self.quantity = int(quantity)
        self.price = Decimal(str(price))
        self.discounted = discounted
        self.original_price = Decimal(str(original_price))

    def __repr__(self):
        return u'CartItem Object (%s)' % self.product

    def to_dict(self):
        return {
            'product_pk': self.product.pk,
            'quantity': self.quantity,
            'price': str(self.price),
            'discounted': self.discounted,
            'original_price': str(self.original_price),
        }

    @property
    def subtotal(self):
        """
        Subtotal for the cart item.
        """
        return self.price * self.quantity


class Cart:

    """
    A cart that lives in the session.
    """
    def __init__(self, session):
        self._items_dict = {}
        self.session = session
        # If a cart representation was previously stored in session, then we
        # rebuild the cart object from that serialized representation.
        if SESSION_KEY in self.session:
            cart_representation = self.session[SESSION_KEY]
            ids_in_cart = cart_representation.keys()
            products_queryset = Product.objects.filter(pk__in=ids_in_cart)
            for product in products_queryset:
                item = cart_representation[str(product.pk)]
                self._items_dict[product.pk] = CartItem(
                    product,
                    item['quantity'],
                    Decimal(item['price']),
                    item.get('discounted', False),
                    Decimal(item.get('original_price', '0')),
                )

    def __contains__(self, product):
        """
        Checks if the given product is in the cart.
        """
        return product in self.products

    def update_session(self):
        """
        Serializes the cart data, saves it to session and marks session as modified.
        """
        self.session[SESSION_KEY] = self.cart_serializable
        self.session.modified = True

    def add(self, product, price=None, quantity=1, discounted=False, original_price='0'):
        """
        Adds or creates products in cart. For an existing product,
        the quantity is increased and the price is ignored.
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')
        if product in self.products:
            self._items_dict[product.pk].quantity += quantity
        else:
            if price == None:
                raise ValueError('Missing price when adding to cart')
            self._items_dict[product.pk] = CartItem(product, quantity, price, discounted, original_price)
        self.update_session()

    def remove(self, product):
        """
        Removes the product.
        """
        if product in self.products:
            del self._items_dict[product.pk]
            self.update_session()

    def remove_single(self, product):
        """
        Removes a single product by decreasing the quantity.
        """
        if product in self.products:
            if self._items_dict[product.pk].quantity <= 1:
                # There's only 1 product left so we drop it
                del self._items_dict[product.pk]
            else:
                self._items_dict[product.pk].quantity -= 1
            self.update_session()

    def clear(self):
        """
        Removes all items.
        """
        self._items_dict = {}
        self.update_session()

    def set_quantity(self, product, quantity):
        """
        Sets the product's quantity.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError('Quantity must be positive when updating cart')
        if product in self.products:
            self._items_dict[product.pk].quantity = quantity
            if self._items_dict[product.pk].quantity < 1:
                del self._items_dict[product.pk]
            self.update_session()

    def set_discounted_price(self, product, discounted_price):
        if product in self.products:
            cart_item = self._items_dict[product.pk]
            cart_item.original_price = cart_item.price
            cart_item.price = Decimal(str(discounted_price))
            cart_item.discounted = True
            self.update_session()

    @property
    def items(self):
        """
        The list of cart items.
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        The serializable representation of the cart.
        For instance:
        {
            '1': {'product_pk': 1, 'quantity': 2, price: '9.99'},
            '2': {'product_pk': 2, 'quantity': 3, price: '29.99'},
        }
        Note how the product pk servers as the dictionary key.
        """
        cart_representation = {}
        for item in self.items:
            # JSON serialization: object attribute should be a string
            product_id = str(item.product.pk)
            cart_representation[product_id] = item.to_dict()
        return cart_representation


    @property
    def items_serializable(self):
        """
        The list of items formatted for serialization.
        """
        return self.cart_serializable.items()

    @property
    def count(self):
        """
        The number of items in cart, that's the sum of quantities.
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        return len(self._items_dict)

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def products(self):
        """
        The list of associated products.
        """
        return [item.product for item in self.items]

    @property
    def total(self):
        """
        The total value of all items in the cart.
        """
        return sum([item.subtotal for item in self.items])