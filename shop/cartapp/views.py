import pdb
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponseRedirect
from django.db.models import Sum
from mainapp.models import Product
from .models import Cart
from mainapp.views import menu


def cart_view(request):
    cart = Cart.objects.filter(user=request.user)
    cart_total = cart.aggregate(Sum("quantity"))["quantity__sum"]
    total_price = sum(
        [product.product.price * product.quantity for product in cart.all()]
    )
    return render(
        request,
        "cartapp/cart.html",
        context={
            "cart": cart,
            "menu": menu,
            "total": cart_total,
            "price": total_price,
        },
    )


def add_item(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product)

    if cart_item:
        cart = cart_item.first()
    else:
        cart = Cart(user=request.user, product=product)

    cart.quantity += 1
    cart.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
