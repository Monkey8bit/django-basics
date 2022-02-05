from unicodedata import category
from urllib import request
from mainapp.models import Product, ProductCategory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from adminapp.forms import ProductCategoryEditForm
from django.urls import reverse


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all()

    return render(
        request,
        "adminapp/category/categories.html",
        context={
            "title": "Admin/categories",
            "categories": categories_list,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    if request.method == "POST":
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse("adminapp:categories"))
    else:
        category_form = ProductCategoryEditForm()

    return render(
        request,
        "adminapp/category/update_category.html",
        context={
            "title": "Admin/category/create",
            "update_form": category_form,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def update_category(request, pk):
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == "POST":
        edit_form = ProductCategoryEditForm(
            request.POST, request.FILES, instance=edit_category
        )

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse("adminapp:update_category", args=[edit_category.pk])
            )
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    return render(
        request,
        "adminapp/category/update_category.html",
        context={"title": "Admin/category/edit", "update_form": edit_form},
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse("adminapp:categories"))

    return render(
        request,
        "adminapp/category/delete_category.html",
        context={
            "title": "Admin/category/delete",
            "category_to_delete": category,
        },
    )
