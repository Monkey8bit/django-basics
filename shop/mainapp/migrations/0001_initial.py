# Generated by Django 3.2.11 on 2022-01-22 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Category name')),
                ('description', models.TextField(blank=True, verbose_name='Category description')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Product name')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Product price')),
                ('color', models.PositiveIntegerField(default=0, verbose_name='Product color')),
                ('description', models.TextField(blank=True, verbose_name='Product description')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Product image')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Product quantity')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='mainapp.productcategory')),
            ],
        ),
    ]
