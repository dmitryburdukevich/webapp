from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    '''
    Вызывается из продукта, откуда и берется product_id.
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        if quantity > product.amount:
            quantity = product.amount
        cart.add(product=product, quantity=quantity, update_quantity=cd['update_quantity'])

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request): 
    cart = Cart(request)

    context = {'cart': cart}

    return render(request, 'cart/cart.html', context)
