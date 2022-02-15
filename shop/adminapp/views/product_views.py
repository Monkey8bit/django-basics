import pdb
from mainapp.models import Product, ProductCategory
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from adminapp.forms import ProductEditForm


class ProductCreateView(CreateView):
    model = Product
    template_name = "adminapp/product/update_product.html"
    fields = (
        "category",
        "name",
        "price",
        "color",
        "description",
        "image",
        "quantity",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context

    def get_initial(self):
        return {"category": self.get_category()}

    def get_category(self):
        return ProductCategory.objects.get(pk=self.kwargs["pk"])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = "adminapp/product/products.html"

    def get_category(self):
        return ProductCategory.objects.get(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.get_category()
        return context

    def get_queryset(self):
        return self.model.objects.filter(category__pk=self.kwargs["pk"])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        # pdb.set_trace()
        return super().dispatch(request, *args, **kwargs)


class ProductView(DetailView):
    model = Product
    template_name = "adminapp/product/read_product.html"


class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"
    template_name = "adminapp/product/update_product.html"


@user_passes_test(lambda u: u.is_superuser)
def create_product(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse("adminapp:products", args=[pk]))
    else:
        product_form = ProductEditForm(initial={"category": category})

    return render(
        request,
        "adminapp/product/update_product.html",
        context={
            "title": "Admin/create",
            "update_form": product_form,
            "category": category,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def read_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "adminapp/product/read_product.html",
        context={
            "title": f"Admin/{product.name}/read",
            "product": product,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("adminapp:update_product", args=[edit_product.pk]))

    else:
        edit_form = ProductEditForm(instance=edit_product)

    return render(
        request,
        "adminapp/product/update_product.html",
        context={
            "title": f"Admin/{edit_product.name}/edit",
            "update_form": edit_form,
            "category": edit_product.category,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse("adminapp:products", args=[product.category.pk]))

    return render(
        request,
        "adminapp/product/delete_product.html",
        context={
            "title": f"Admin/{product.name}/delete",
            "product_to_delete": product,
            "category": product.category,
        },
    )
