from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all()

    return render(
        request,
        "adminapp/user/users.html",
        context={
            "title": "Admin/users",
            "users": users_list,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("adminapp:users"))
    else:
        user_form = ShopUserRegisterForm()

    return render(
        request,
        "adminapp/user/update_user.html",
        context={
            "title": "Admin/user/create",
            "update_form": user_form,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def update_user(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        edit_form = ShopUserAdminEditForm(
            request.POST, request.FILES, instance=edit_user
        )

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse("adminapp:update_user", args=[edit_user.pk])
            )
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    return render(
        request,
        "adminapp/user/update_user.html",
        context={"title": "Admin/user/edit", "update_form": edit_form},
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("adminapp:users"))

    return render(
        request,
        "adminapp/user/delete_user.html",
        context={
            "title": "Admin/user/delete",
            "user_to_delete": user,
        },
    )
