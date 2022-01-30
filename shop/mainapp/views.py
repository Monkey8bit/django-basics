from django.shortcuts import get_object_or_404, render
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
    category = ProductCategory.objects.all()
    return render(
        request,
        "mainapp/products.html",
        context={
            "title": "Products",
            "menu": menu,
            "products": products,
            "categories": category,
        },
    )


def category(request, pk):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category=category)
    return render(
        request,
        "mainapp/products.html",
        context={
            "title": "Products",
            "menu": menu,
            "products": products,
            "categories": categories,
        },
    )


def contact(request):
    return render(
        request,
        "mainapp/contact.html",
        context={"title": "Contacts", "menu": menu},
    )
