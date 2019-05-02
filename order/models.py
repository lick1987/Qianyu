from django.db import models
from index.models import *
from source.models import *
# Create your models here.
#订单总表
class order(models.Model):
    user=models.ForeignKey(user,True)
    customer=models.ForeignKey(customer,True)
    unit=models.ForeignKey(unit,True)
    source=models.ForeignKey(source,True)
    count=models.CharField(max_length=100,verbose_name='数量')
    #状态
    status = models.CharField(max_length=20, verbose_name='状态')
    #接单时间
    startTime = models.CharField(max_length=50,verbose_name='接单时间')
    #完结时间
    endTime=models.CharField(max_length=50,verbose_name='预期完结时间')
    explain=models.CharField(max_length=300,verbose_name='备注',default='')
    #发票类型
    style=models.CharField(max_length=10,verbose_name='发票类型',default='纸质发票')
    isActive = models.BooleanField(default=True, verbose_name='状态')
    def __str__(self):
        return str(self.customer)

    class Meta:
        app_label='order'
        verbose_name = '订单总表'
        verbose_name_plural = verbose_name