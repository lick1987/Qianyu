# Generated by Django 2.2 on 2019-05-06 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20190506_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='uTax',
            field=models.CharField(default='4', max_length=10, verbose_name='发票点子'),
        ),
    ]
