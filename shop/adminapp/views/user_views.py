from django.shortcuts import HttpResponseRedirect
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator

from adminapp.forms import ShopUserAdminEditForm, ShopUserAdminCreateForm


class UserListView(ListView):
    model = ShopUser
    template_name = "adminapp/user/users.html"

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = "adminapp/user/update_user.html"
    form_class = ShopUserAdminCreateForm
    success_url = reverse_lazy("adminapp:users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Admin/create"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = "adminapp/user/update_user.html"
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy("adminapp:users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.object.username
        context["title"] = f"Admin/{user_name}/edit"
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = "adminapp/user/delete_user.html"
    success_url = reverse_lazy("adminapp:users")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
