# Generated by Django 2.2 on 2019-05-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_auto_20190512_0123'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sourceName',
            field=models.CharField(default='暂无', max_length=100, verbose_name='开票员'),
        ),
    ]
