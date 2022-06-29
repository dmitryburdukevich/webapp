from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderCreateForm
from .models import OrderItem, Order
from django.contrib import messages
from cart.cart import Cart


def order_create(request):
    # 1) Get/create a cart
    cart = Cart(request)
    if request.method == "POST":
        # 2) Validate request
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 3) Save
            order = form.save(commit=False)
            if request.user.is_authenticated:
                cd = form.cleaned_data
                order.user = request.user
            order.save()
            # 4) Move products to order items
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            # 5) Remove products from cart
            cart.clear()

            messages.success(request, 'Success: Order added')
            if request.user.is_authenticated:
                orders = Order.objects.filter(user=request.user)
                context = {'order': order, 'orders': orders}
                return render(request,'orders/orders.html', context)
            else:
                context = {'order': order}
                return redirect('orders:order_specific', order.id)
    else:
        form = OrderCreateForm()
        return render(request, 'orders/create.html', {'cart': cart, 'form': form})


def order_specific(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('product')
    context = {'order': order, 'order_items': order_items}

    return render(request, 'orders/order.html', context)


def order_all(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'orders/orders.html', context)

