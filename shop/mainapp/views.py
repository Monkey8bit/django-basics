from unicodedata import name
from django.shortcuts import render


menu = [
    {"name": "домой", "link": "index"},
    {"name": "продукты", "link": "product"},
    {"name": "контакты", "link": "contact"},
]

def index(request):
    return render(request, "mainapp/index.html", context={
        "menu": menu
    })

def product(request):
    products = [
        {"name": "Отличный стул", "link": "static/img/product-11.jpg"},
        {"name": "Отличный стул", "link": "static/img/product-21.jpg"},
        {"name": "Отличный стул", "link": "static/img/product-21.jpg"},
        
    ]
    return render(request, "mainapp/products.html", context={
        "menu": menu,
        "products": products
    })

def contact(request):
    return render(request, "mainapp/contact.html", context={
        "menu": menu
    })
