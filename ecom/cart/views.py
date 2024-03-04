from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.contrib import messages
from .cart import Cart


# Create your views here.
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products,
                                                 "quantities": quantities,
                                                 "totals": totals
                                                 })


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get cart Quantity
        cart_quantity = cart.__len__()

        # return response
        # response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product added to cart...")
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({"product_id": product_id})
        messages.success(request, "Item has been Deleted from the cart...")
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({"qrt": product_qty})
        messages.success(request, "Your cart has been updated...")
        return response
    # return redirect('cart_summary')
