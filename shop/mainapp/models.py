from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="Category name", max_length=100)
    description = models.TextField(
        verbose_name="Category description", blank=True
    )

    class Meta:
        verbose_name_plural = "Product categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, blank=True
    )
    name = models.CharField(verbose_name="Product name", max_length=120)
    price = models.DecimalField(
        verbose_name="Product price", max_digits=6, decimal_places=2, default=0
    )
    color = models.PositiveIntegerField(
        verbose_name="Product color", default=0x000000
    )
    description = models.TextField(
        verbose_name="Product description", blank=True
    )
    image = models.ImageField(
        verbose_name="Product image", blank=True, upload_to="products"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Product quantity", default=0
    )

    def __str__(self):
        return self.name
