from django.core import serializers
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
import os


JSON_PATH = "mainapp/json"


def json_serialize(model):
    data = serializers.serialize("json", model)
    return data


class Command(BaseCommand):
    def handle(self, *args, **options):
        json_categories = json_serialize(ProductCategory.objects.all())
        json_products = json_serialize(Product.objects.all())

        with open(
            os.path.join(JSON_PATH, "categories" + ".json"), "w"
        ) as category_json:
            category_json.write(json_categories)

        with open(
            os.path.join(JSON_PATH, "products" + ".json"), "w"
        ) as products_json:
            products_json.write(json_products)
