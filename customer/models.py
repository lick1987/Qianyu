from django.db import models
from index.models import *
# Create your models here.
#查询单位总表
class userCusterData(models.Model):
    user=models.ForeignKey(user,True)
    customer=models.ForeignKey(customer,True)
    isActive = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return str(self.customer)
    class Meta:
        verbose_name = '总表'
        verbose_name_plural = verbose_name
