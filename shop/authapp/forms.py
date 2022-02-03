from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "password")

    def __init__(self, *args, **kwargs) -> None:
        super(ShopUserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "password1",
            "password2",
            "email",
            "age",
            "city",
            "phone",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super(ShopUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            "username",
            "first_name",
            "password",
            "email",
            "age",
            "city",
            "phone",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if field_name == "password":
                field.widget = forms.HiddenInput()
