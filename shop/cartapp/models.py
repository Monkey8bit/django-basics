from functools import lru_cache
from django.db import models
from django.conf import settings
from mainapp.models import Product


class CartQuerySet(models.query.QuerySet):

    def delete(self, *args, **kwargs):
        item: Cart
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()

        super().delete(*args, **kwargs)


class CartManager(models.Manager):
    """Manager for products in cart of specific user"""

    @lru_cache
    def total_price(self):
        """Returns total price of user cart."""
        return sum(item.product.price * item.quantity for item in self.all())

    @lru_cache
    def total_cart_items(self):
        """Returns total count of products in user cart."""
        cart_items = self.all()
        return sum(item.quantity for item in cart_items)

    def get_queryset(self):
        return CartQuerySet(self.model, using=self._db)


class Cart(models.Model):
    """Model for product in cart."""

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

    def save(self, *args, **kwargs):
        if self.pk:
            old_cart = Cart.objects.get(pk=self.pk)
            self.product.quantity -= (self.quantity - old_cart.quantity)
        else:
            self.product.quantity -= self.quantity
        self.product.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    @property
    def product_price(self):
        """Returns total price of product depending of quantity."""
        return self.product.price * self.quantity

    @staticmethod
    def get_cart(user):
        """Returns query of all products in user's cart."""
        return Cart.objects.all().filter(user=user)
