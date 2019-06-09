from django.db import models

# Create your models here.
from django.db import models
from index.models import *
# Create your models here.


#加油员表
class tomorrow(models.Model):
    times = models.CharField(max_length=11,verbose_name='日期')
    arrange = models.CharField(max_length=20,verbose_name='具体金额')
    customerUnit = models.CharField(max_length=20,verbose_name='单位')
    customerPwd=models.CharField(max_length=200,verbose_name='税号')
    sourceName=models.CharField(max_length=10,verbose_name='开票员')
    customerName=models.CharField(max_length=10,verbose_name='顾客姓名')
    explain=models.CharField(max_length=500,verbose_name='要求')
    isChange=models.BooleanField(default=True,verbose_name='是否改变')
    isActive = models.BooleanField(default=True,verbose_name='状态')
    def __str__(self):
        return str(self.times)
    class Meta:
        app_label = 'tomorrow'
        verbose_name = '明日安排'
        verbose_name_plural = verbose_name
    def to_dic(self):
        dic = {}
        dic['id'] = self.id
        # 接单时间
        dic['times'] = self.times
        dic['arrange'] = self.arrange
        dic['customerUnit'] = self.customerUnit
        dic['customerPwd'] = self.customerPwd
        dic['sourceName'] = self.sourceName
        dic['customerName'] = self.customerName
        dic['explain'] = self.explain
        return dic