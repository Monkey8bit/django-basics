# Generated by Django 3.2.11 on 2022-02-19 20:36

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20220216_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='key_expires',
            field=models.DateTimeField(default=authapp.models.get_expiration_time),
        ),
    ]