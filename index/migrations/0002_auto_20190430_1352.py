# Generated by Django 2.2 on 2019-04-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='uphone',
            field=models.CharField(max_length=50, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='uqq',
            field=models.CharField(max_length=15, verbose_name='QQ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='count',
            field=models.CharField(max_length=100, verbose_name='数量'),
        ),
    ]
