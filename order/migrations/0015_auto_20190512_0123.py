# Generated by Django 2.2 on 2019-05-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20190510_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='source',
        ),
        migrations.RemoveField(
            model_name='order',
            name='unit',
        ),
        migrations.AddField(
            model_name='order',
            name='customerAddress',
            field=models.CharField(default='暂无', max_length=100, verbose_name='客户地址'),
        ),
        migrations.AddField(
            model_name='order',
            name='customerName',
            field=models.CharField(default='暂无', max_length=100, verbose_name='客户姓名'),
        ),
        migrations.AddField(
            model_name='order',
            name='customerPwd',
            field=models.CharField(default='暂无', max_length=100, verbose_name='客户税号'),
        ),
        migrations.AddField(
            model_name='order',
            name='customerUnit',
            field=models.CharField(default='暂无', max_length=100, verbose_name='客户单位'),
        ),
        migrations.AddField(
            model_name='order',
            name='orderName',
            field=models.CharField(default='微信-李旭', max_length=100, verbose_name='接单账号'),
        ),
    ]
