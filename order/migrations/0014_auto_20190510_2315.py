# Generated by Django 2.2 on 2019-05-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_order_utax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notComple',
            field=models.IntegerField(default=0, verbose_name='完成情况'),
        ),
    ]
