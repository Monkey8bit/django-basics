from django.conf import settings
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from functools import lru_cache

from cartapp.models import Cart
from .models import Product, ProductCategory


@lru_cache
def get_product(category="all"):
    if category == "all":
        return Product.objects.all()[:4]
    return Product.objects.filter(category_id=category)


def get_category(pk=None):
    if settings.LOW_CACHE:
        if pk:
            KEY = f"category_{pk}"
            category = cache.get(KEY)
            if not category:
                category = ProductCategory.objects.filter(pk=pk)
                cache.set(KEY, category)
            return category
        KEY = "all_categories"
        categories = cache.get(KEY)
        if not categories:
            categories = ProductCategory.objects.all()
            cache.set(KEY, categories)
        return categories
    return ProductCategory.objects.filter(pk=pk) if pk else \
            ProductCategory.objects.all()

def index(request):
    """View for main page."""
    product = get_product()
    return render(
        request,
        "mainapp/index.html",
        context={
            "title": "Main",
            "products": product,
        },
    )


def product(request, pk=None, page=1):
    """View for products page."""
    products = get_product(pk) if pk else Product.objects.all()
    hot_product = Product.random_product(products)
    categories = get_category()

    if pk is not None:
        if pk == 0:
            category = {
                "pk": 0,
                "name": "all",
            }
            products = Product.objects.filter(is_active=True)
        else:
            category = get_category(pk=pk)
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
            "products": products_paginator,
            "categories": categories,
            "category": category,
            "hot_product": hot_product,
        }

    except UnboundLocalError:
        content = {
            "title": "Products",
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
        },
    )


def category(request, pk):
    """View for page products, used for display specific category of product"""
    categories = get_category()
    category = get_category(pk=pk)
    products = Product.objects.filter(category=category)
    hot_product = Product.random_product(Product.objects.filter(category=category))

    return render(
        request,
        "mainapp/products.html",
        context={
            "title": "Products",
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
        context={
            "title": "Contacts",
        },
    )
