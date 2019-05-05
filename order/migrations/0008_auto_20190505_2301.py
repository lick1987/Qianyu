# Generated by Django 2.2 on 2019-05-05 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='actualCost',
            field=models.IntegerField(default=0, max_length=100, verbose_name='实际成本'),
        ),
        migrations.AddField(
            model_name='order',
            name='actualProfit',
            field=models.IntegerField(default=0, max_length=100, verbose_name='实际利润'),
        ),
        migrations.AddField(
            model_name='order',
            name='estimatProfit',
            field=models.IntegerField(default=0, max_length=100, verbose_name='预计利润'),
        ),
        migrations.AddField(
            model_name='order',
            name='estimateCost',
            field=models.IntegerField(default=0, max_length=100, verbose_name='预计成本'),
        ),
        migrations.AddField(
            model_name='order',
            name='netReceiots',
            field=models.IntegerField(default=0, max_length=100, verbose_name='实收'),
        ),
        migrations.AddField(
            model_name='order',
            name='recivable',
            field=models.IntegerField(default=0, max_length=100, verbose_name='应收'),
        ),
    ]
