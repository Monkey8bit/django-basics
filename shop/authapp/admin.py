from atexit import register
from django.contrib import admin

from authapp.models import ShopUser


admin.site.register(ShopUser)
