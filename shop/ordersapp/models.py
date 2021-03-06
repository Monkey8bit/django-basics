import pdb
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.conf import settings
from cartapp.models import Cart, Product


class Order(models.Model):

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ("-created",)

    CREATED = "CREATED"
    IN_PROCESS = "IN_PROCESS"
    PAYMENT_AWAITING = "PAIMENT_AWAITING"
    PAID = "PAID"
    READY = "READY"
    CANCELLED = "CANCELLED"
    FINISHED = "FINISHED"

    ORDER_STATUS_CHOICES = (
        (CREATED, "Created"),
        (IN_PROCESS, "In process"),
        (PAYMENT_AWAITING, "Payment awaiting"),
        (PAID, "Paid"),
        (READY, "Ready"),
        (CANCELLED, "Cancelled"),
        (FINISHED, "Finished"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Updated", auto_now=True)
    status = models.CharField(verbose_name="Status", choices=ORDER_STATUS_CHOICES, max_length=20, default=CREATED)
    is_active = models.BooleanField(verbose_name="Is active", default=True)

    def __str__(self):
        return f"Order №{self.id}"

    def get_total_cost(self):
        return sum(item.cost for item in self.items.select_related())

    def get_total_quantity(self):
        items = self.items.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.items.select_related()
        return len(items)

    def delete(self):
        for item in self.items.select_related("product"):
            item.delete()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", default=0)

    @property
    def cost(self):
        return self.product.price * self.quantity


@receiver(pre_save, sender=OrderItem)
def save_item(sender, update_fields, instance: OrderItem, **kwargs):
    if instance.pk:
        old_item = OrderItem.objects.get(pk=instance.pk)
        instance.product.quantity -= instance.quantity - old_item.quantity
    else:
        instance.product.quantity -= instance.quantity

    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def delete_item(sender, instance: OrderItem, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
