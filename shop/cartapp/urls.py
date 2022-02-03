from django.urls import path
from . import views as cartapp


app_name = "cartapp"

urlpatterns = [
    path("", cartapp.cart_view, name="cart"),
    path("add/<int:product_id>/", cartapp.add_item, name="add"),
    path("remove/<int:cart_item_id>/", cartapp.remove_item, name="remove"),
    path(
        "edit/<int:cart_item_id>/<int:quantity>/",
        cartapp.edit_item,
        name="edit",
    ),
]
