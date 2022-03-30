import pdb
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)
from django.forms import inlineformset_factory
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse
)
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse_lazy, reverse

from functools import lru_cache
from cartapp.models import Cart
from mainapp.models import Product
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm


class OrderEditMixin:
    @lru_cache()
    def make_formset(self, instance=None):
        OrderFormSet = inlineformset_factory(
            Order, OrderItem, form=OrderItemForm, extra=0
        )

        formset = OrderFormSet(instance=instance)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=instance)
        else:
            if not instance:
                cart_items = Cart.get_cart(self.request.user)
                if len(cart_items):
                    OrderFormSet = inlineformset_factory(
                        Order, OrderItem, form=OrderItemForm, extra=len(cart_items)
                    )
                    formset = OrderFormSet()
                    for num, form in enumerate(formset.forms):
                        form.initial["product"] = cart_items[num].product
                        form.initial["quantity"] = cart_items[num].quantity
                        form.initial["price"] = cart_items[num].product_price
                    cart_items.delete()
            
        self.add_price_to_formset_forms(formset)
        return formset
    
    def add_price_to_formset_forms(self, formset):
        for form in formset.forms:
            if form.instance.pk:
                form.initial["price"] = form.instance.product.price
        return formset

    def save_formset(self, form, formset):
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        if not self.object.get_total_cost():
            self.object.delete()


class OrderCreate(OrderEditMixin, CreateView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        data = super(OrderCreate, self).get_context_data(**kwargs)

        data["orderitems"] = self.make_formset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        self.save_formset(form, orderitems)

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(OrderEditMixin, UpdateView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        data = super(OrderUpdate, self).get_context_data(**kwargs)

        data["orderitems"] = self.make_formset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context["orderitems"]

        self.save_formset(form, orderitems)

        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy("ordersapp:orders_list")


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetail(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_quantity"] = self.object.get_total_quantity()
        context["order_price"] = self.object.get_total_cost()
        return context


def order_forming_complete(request, pk):
    orders = Order.objects.filter(user=request.user)
    order = get_object_or_404(orders, pk=pk)
    if order.status != Order.CREATED:
        return HttpResponseBadRequest()
    order.status = Order.IN_PROCESS
    order.save()
    return HttpResponseRedirect(reverse("ordersapp:orders_list"))


def product_price(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({
        "price": product.price
    })
