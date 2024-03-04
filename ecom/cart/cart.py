from store.models import Product, Profile
from decimal import Decimal


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Get the current session key if it exist
        cart = self.session.get('session_key')

        # if the user is new, no session key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Make sure cart is available on all pages of site
        self.cart = cart
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #     save carty to the profile model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #     save carty to the profile model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup product in db
        products = Product.objects.filter(id__in=product_ids)
        # return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # get cart
        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # lookup these keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            # convert key string into so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += Decimal(product.sale_price) * Decimal(value)
                    else:
                        total += Decimal(product.price) * Decimal(value)
        return total
