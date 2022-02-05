import adminapp.views as adminapp
from django.urls import path

app_name = "adminapp"

urlpatterns = [
    path("users/create/", adminapp.create_user, name="create_user"),
    path("users/read/", adminapp.users, name="users"),
    path("users/update/<int:pk>/", adminapp.update_user, name="update_user"),
    path("users/delete/<int:pk>/", adminapp.delete_user, name="delete_user"),
    path(
        "categories/create/", adminapp.create_category, name="create_category"
    ),
    path("categories/read/", adminapp.categories, name="categories"),
    path(
        "categories/update/<int:pk>/",
        adminapp.update_category,
        name="update_category",
    ),
    path(
        "categories/delete/<int:pk>/",
        adminapp.delete_category,
        name="delete_category",
    ),
    path(
        "products/create/category/<int:pk>/",
        adminapp.create_product,
        name="create_product",
    ),
    path(
        "products/read/category/<int:pk>/", adminapp.products, name="products"
    ),
    path(
        "products/read/<int:pk>/", adminapp.read_product, name="read_product"
    ),
    path(
        "products/update/<int:pk>/",
        adminapp.update_product,
        name="update_product",
    ),
    path(
        "products/delete/<int:pk>/",
        adminapp.delete_product,
        name="delete_product",
    ),
]
