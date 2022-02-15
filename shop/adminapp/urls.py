import adminapp.views as adminapp
from django.urls import path

app_name = "adminapp"

urlpatterns = [
    path("users/create/", adminapp.UserCreateView.as_view(), name="create_user"),
    path("users/read/", adminapp.UserListView.as_view(), name="users"),
    path("users/update/<int:pk>/", adminapp.UserUpdateView.as_view(), name="update_user"),
    path("users/delete/<int:pk>/", adminapp.UserDeleteView.as_view(), name="delete_user"),
    path(
        "categories/create/",
        adminapp.create_category,
        name="create_category",
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
        adminapp.ProductCreateView.as_view(),
        name="create_product",
    ),
    path("products/read/category/<int:pk>/", adminapp.ProductListView.as_view(), name="products"),
    path("products/read/<int:pk>/", adminapp.ProductView.as_view(), name="read_product"),
    path(
        "products/update/<int:pk>/",
        adminapp.ProductUpdateView.as_view(),
        name="update_product",
    ),
    path(
        "products/delete/<int:pk>/",
        adminapp.delete_product,
        name="delete_product",
    ),
]
