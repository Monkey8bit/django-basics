from django.urls import path
import mainapp.views as mainapp


app_name = "mainapp"

urlpatterns = [
    path("", mainapp.product, name="index"),
    path("<int:pk>/", mainapp.category, name="category"),
    path("product/<int:pk>/", mainapp.product_page, name="product"),
]
