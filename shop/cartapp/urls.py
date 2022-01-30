from django.urls import path
from . import views


app_name = "cartapp"

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<int:product_id>", views.add_item, name="add"),
    path("remove/<int:cart_item_id>", views.remove_item, name="remove"),
]
