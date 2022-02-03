from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from mainapp.models import Product
from .models import Cart
from mainapp.views import menu


@login_required
def cart_view(request):
    cart = Cart.get_cart(request.user)
    return render(
        request,
        "cartapp/cart.html",
        context={
            "cart": cart,
            "menu": menu,
        },
    )


@login_required
def add_item(request, product_id):
    if "login" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(
            reverse("products:product", args=[product_id])
        )

    product = get_object_or_404(Product, pk=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product)

    if cart_item:
        cart = cart_item.first()
    else:
        cart = Cart(user=request.user, product=product)

    cart.quantity += 1
    cart.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def edit_item(request, cart_item_id, quantity):
    if request.is_ajax():
        new_cart_item = Cart.objects.get(pk=cart_item_id)

        if quantity:
            new_cart_item.quantity = quantity
            new_cart_item.save()
        else:
            new_cart_item.delete()

    cart = Cart.get_cart(user=request.user)

    return render(
        request,
        "cartapp/includes/inc_cart.html",
        context={
            "cart": cart,
        },
    )
