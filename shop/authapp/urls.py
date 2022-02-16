from django.urls import path, re_path
from . import views as authapp


app_name = "authapp"

urlpatterns = [
    path("login/", authapp.login, name="login"),
    path("logout/", authapp.logout, name="logout"),
    path("registration/", authapp.registration, name="registration"),
    path("edit/", authapp.edit, name="edit"),
    re_path(r"^verify/(?P<email>.+)/(?P<activation_key>\w+)", authapp.verify, name="verify"),
]
