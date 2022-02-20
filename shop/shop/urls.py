from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include

from mainapp import views as mainapp


urlpatterns = [
    path("", include("social_django.urls", namespace="social")),
    path("adminapp/", include("adminapp.urls", namespace="custom_admin")),
    path("", mainapp.index, name="index"),
    path("contact/", mainapp.contact, name="contact"),
    path("product/", include("mainapp.urls", namespace="product")),
    path("auth/", include("authapp.urls", namespace="auth")),
    path("cart/", include("cartapp.urls", namespace="cart")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
