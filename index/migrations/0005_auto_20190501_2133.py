# Generated by Django 2.2 on 2019-05-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_customer_utax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='uaddres',
            field=models.CharField(max_length=200, verbose_name='收货地址'),
        ),
    ]
