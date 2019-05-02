from django.db import models
from index.models import *
# Create your models here.


#加油员表
class source(models.Model):
    uphone = models.CharField(max_length=11,verbose_name='手机号')
    uwei = models.CharField(max_length=20,verbose_name='微信')
    uname = models.CharField(max_length=20,verbose_name='用户名')
    uaddres=models.CharField(max_length=200,verbose_name='加油站地址')
    uchoice=models.CharField(max_length=10,verbose_name='发票类型',default='纸质发票')
    uTax=models.CharField(max_length=10,verbose_name='发票点子',default='3')

    isActive = models.BooleanField(default=True,verbose_name='状态')
    def __str__(self):
        return str(self.uname)
    class Meta:
        verbose_name = '加油员信息'
        verbose_name_plural = verbose_name
#查询单位总表
class userSourceData(models.Model):
    user=models.ForeignKey(user,True)
    source=models.ForeignKey(source,True)
    isActive = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return str(self.source)
    class Meta:
        verbose_name = '加油员总表'
        verbose_name_plural = verbose_name

