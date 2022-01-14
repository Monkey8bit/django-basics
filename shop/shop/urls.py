from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", mainapp.index),
    path("contacts/", mainapp.contact),
    path("products/", mainapp.product),
]
