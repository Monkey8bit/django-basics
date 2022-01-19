from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", mainapp.index, name="index"),
    path("contact/", mainapp.contact, name="contact"),
    path("product/", mainapp.product, name="product"),
]
