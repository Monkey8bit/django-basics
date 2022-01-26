from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.core import serializers

import os


JSON_PATH = 'mainapp/json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(JSON_PATH, 'categories.json'), 'r') as categories_json:
            categories = serializers.deserialize('json', categories_json)
            ProductCategory.objects.all().delete()
            for category in categories:
                category.save()
                
        with open(os.path.join(JSON_PATH, 'products.json'), 'r') as products_json:
            products = serializers.deserialize("json", products_json)
            Product.objects.all().delete()
            for product in products:
              product.save()

       