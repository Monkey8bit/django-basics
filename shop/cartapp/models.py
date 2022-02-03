from django.db import models
from django.conf import settings
from mainapp.models import Product


class CartManager(models.Manager):
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.all())

    def total_cart_items(self):
        cart_items = self.all()
        return sum(item.quantity for item in cart_items)


class Cart(models.Model):
    class Meta:
        unique_together = ["user", "product"]

    objects = CartManager()

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

    @property
    def product_price(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_cart(user):
        return Cart.objects.all().filter(user=user)
