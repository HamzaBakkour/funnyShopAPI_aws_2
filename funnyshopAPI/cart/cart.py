from decimal import Decimal
from django.conf import settings
from shop.models import Product
from shop.serializers import ProductSerializer

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart



    def __len__(self):
        #Count all items in the cart.
        return sum(item['quantity'] for item in self.cart.values())

    
    def get_cart_items(self):
        return self.cart

    def item_exist(self, product_id):
        #Check if a product is in the cart.
        return str(product_id) in self.cart


    def add(self, product, quantity=1, product_image = 'no image', override_quantity=False):
        #Add a product to the cart or update its quantity.
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                        'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.cart[product_id]['product_image'] = product_image
        self.cart[product_id]['name'] = str(product.name)
        self.save()



    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        #Remove a product from the cart.
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    





