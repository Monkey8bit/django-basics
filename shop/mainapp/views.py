from django.shortcuts import render
from .models import Product, ProductCategory


menu = [
    {"name": "home", "link": "index"},
    {"name": "product", "link": "product:index"},
    {"name": "contacts", "link": "contact"},
]

def index(request):
    product = Product.objects.all()

    return render(request,
     "mainapp/index.html",
      context={
        "title": "Главная",
        "menu": menu,
        "products": product,
    })

def product(request, pk=None):
    products = [
        {"name": "Отличный стул", "link": "static/img/product-11.jpg"},
        {"name": "Отличный стул", "link": "static/img/product-21.jpg"},
        {"name": "Отличный стул", "link": "static/img/product-21.jpg"},
        
    ]
    category = ProductCategory.objects.all()
    return render(request, "mainapp/products.html", context={
        "title": "Продукты",
        "menu": menu,
        "products": products,
        "categories": category,
        "pk": pk,
    })

def contact(request):
    return render(request, "mainapp/contact.html", context={
        "title": "Контакты",
        "menu": menu
    })
