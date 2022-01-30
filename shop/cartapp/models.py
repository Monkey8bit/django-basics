from django.db import models
from django.conf import settings
from mainapp.models import Product


class Cart(models.Model):
    class Meta:
        unique_together = ["user", "product"]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", default=0)
    add_datetime = models.DateTimeField(verbose_name="Time", auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"
