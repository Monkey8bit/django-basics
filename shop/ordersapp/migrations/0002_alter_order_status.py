# Generated by Django 3.2.11 on 2022-02-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('IN_PROCESS', 'In process'), ('PAIMENT_AWAITING', 'Paymen awaiting'), ('PAID', 'Paid'), ('READY', 'Ready'), ('CANCELLED', 'Cancelled'), ('FINISHED', 'Finished')], default='CREATED', max_length=20, verbose_name='Status'),
        ),
    ]