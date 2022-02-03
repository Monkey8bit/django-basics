from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse

from cartapp.models import Cart
from .models import Product, ProductCategory


menu = [
    {"name": "home", "link": "index", "active": ["index"]},
    {
        "name": "product",
        "link": "product:index",
        "active": ["product:category", "product:index"],
    },
    {"name": "contacts", "link": "contact", "active": ["contact"]},
]


def index(request):
    product = Product.objects.all()
    return render(
        request,
        "mainapp/index.html",
        context={
            "title": "Main",
            "menu": menu,
            "products": product,
        },
    )


def product(request):
    products = Product.objects.all()
    hot_product = Product.random_product(products)
    category = ProductCategory.objects.all()
    return render(
        request,
        "mainapp/products.html",
        context={
            "title": "Products",
            "menu": menu,
            "products": products,
            "categories": category,
            "hot_product": hot_product,
        },
    )


def product_page(request, pk):
    title = "Product page"
    product = get_object_or_404(Product, pk=pk)
    try:
        cart = Cart.get_cart(user=request.user)
    except TypeError:
        return HttpResponseRedirect(reverse("authapp:login"))

    return render(
        request,
        "mainapp/product_page.html",
        context={
            "title": title,
            "product": product,
            "cart": Cart.get_cart(user=request.user),
            "menu": menu,
        },
    )


def category(request, pk):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category=category)
    hot_product = Product.random_product(
        Product.objects.filter(category=category)
    )

    return render(
        request,
        "mainapp/products.html",
        context={
            "title": "Products",
            "menu": menu,
            "products": products,
            "categories": categories,
            "hot_product": hot_product,
        },
    )


def contact(request):
    return render(
        request,
        "mainapp/contact.html",
        context={"title": "Contacts", "menu": menu},
    )
