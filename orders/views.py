from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .models import CartItem, Order, OrderItem
from .forms import CheckoutForm

#Create your views here
def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = _get_session_key(request)

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={"quantity": 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("view_cart")

def view_cart(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, "orders/cart.html", {"cart_items": cart_items, "total": total})

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("view_cart")

def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect("view_cart")


@login_required
def checkout(request):
    session_key = _get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart_items.delete()
            return redirect("order_success", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, "orders/checkout.html", {"form": form, "cart_items": cart_items})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})
