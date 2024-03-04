from .cart import Cart


# create context processor so cart can work on all pages of the site

def cart(request):
    # Return the default data from the cart
    return {'cart': Cart(request)}
