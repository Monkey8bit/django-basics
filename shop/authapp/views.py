from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm


def login(request):
    next = request.GET["next"] if "next" in request.GET.keys() else ""

    if request.method == "POST":
        login_form = ShopUserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]

            user = auth.authenticate(
                request, username=username, password=password
            )
            if user and user.is_active:
                auth.login(request, user)
                if "next" in request.POST.keys():
                    return HttpResponseRedirect(request.POST["next"])
                return HttpResponseRedirect(reverse("index"))
    else:
        login_form = ShopUserLoginForm()

    return render(
        request,
        "authapp/login.html",
        context={
            "title": "Log in",
            "form": login_form,
            "next": next,
        },
    )


def registration(request):
    if request.method == "POST":
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse("auth:login"))
    else:
        register_form = ShopUserRegisterForm()

    return render(
        request,
        "authapp/register.html",
        context={
            "title": "Sign in",
            "form": register_form,
        },
    )


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("index"))


def edit(request):
    if request.method == "POST":
        edit_form = ShopUserEditForm(
            request.POST, request.FILES, instance=request.user
        )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    return render(
        request,
        "authapp/edit.html",
        context={
            "title": "Profile edit",
            "form": edit_form,
        },
    )
