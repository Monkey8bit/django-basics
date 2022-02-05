from mainapp.models import Product, ProductCategory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk)

    return render(
        request,
        "adminapp/product/products.html",
        context={
            "title": "Admin/products",
            "category": category,
            "products": products_list,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def create_product(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def read_product(requst, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    pass
