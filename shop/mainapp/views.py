import pdb
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    """View for main page."""
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


def product(request, pk=None, page=1):
    """View for products page."""
    products = (
        Product.objects.filter(category__pk=pk)
        if pk
        else Product.objects.all()
    )
    hot_product = Product.random_product(products)
    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            category = {
                "pk": 0,
                "name": "all",
            }
            products = Product.objects.filter(is_active=True)
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True)

    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    try:
        content = {
            "title": "Products",
            "menu": menu,
            "products": products_paginator,
            "categories": categories,
            "category": category,
            "hot_product": hot_product,
        }

    except UnboundLocalError:
        content = {
            "title": "Products",
            "menu": menu,
            "products": products_paginator,
            "categories": categories,
            "category": {
                "pk": 0,
                "name": "all",
            },
            "hot_product": hot_product,
        }

    return render(request, "mainapp/products.html", context=content)


def product_page(request, pk):
    """View for specific product."""
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
            "cart": cart,
            "menu": menu,
        },
    )


def category(request, pk):
    """View for page products, used for display specific category of product"""
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
    """View for contacts page."""
    return render(
        request,
        "mainapp/contact.html",
        context={"title": "Contacts", "menu": menu},
    )
