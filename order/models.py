from django.db import models
from index.models import *
from source.models import *
# Create your models here.
#订单总表
class order(models.Model):
    user=models.ForeignKey(user,True)
    # customer=models.ForeignKey(customer,True)
    # unit=models.ForeignKey(unit,True)
    # source=models.ForeignKey(source,True)
    #接单账号
    orderName=models.CharField(max_length=100,verbose_name='接单账号',default='微信-李旭')
    customerName=models.CharField(max_length=100,verbose_name='客户姓名',default='暂无')
    customerUnit=models.CharField(max_length=100,verbose_name='客户单位',default='暂无')
    customerPwd=models.CharField(max_length=100,verbose_name='客户税号',default='暂无')
    customerAddress=models.CharField(max_length=100,verbose_name='客户地址',default='暂无')
    sourceName=models.CharField(max_length=100,verbose_name='开票员',default='暂无')
    count=models.CharField(max_length=100,verbose_name='数量')
    #状态
    status = models.CharField(max_length=20, verbose_name='状态')
    notComple = models.IntegerField(verbose_name='完成情况',default=0)
    #接单时间
    startTime = models.CharField(max_length=50,verbose_name='接单时间')
    #完结时间
    endTime=models.CharField(max_length=50,verbose_name='预期完结时间')
    explain=models.CharField(max_length=300,verbose_name='备注',default='')
    #发票类型
    style=models.CharField(max_length=10,verbose_name='发票类型',default='纸质发票')
    uTax = models.CharField(max_length=10, verbose_name='发票点子', default='4')
    #应收
    recivable = models.IntegerField(verbose_name='应收', default=0)
    #实收

    netReceiots=models.IntegerField( verbose_name='实收', default=0)
    estimateCost=models.IntegerField( verbose_name='预计成本', default=0)
    actualCost=models.IntegerField( verbose_name='实际成本', default=0)
    estimatProfit=models.IntegerField( verbose_name='预计利润', default=0)
    Delivery=models.CharField(max_length=10,verbose_name='发货方式',default='韵达快递')
    actualProfit=models.IntegerField(verbose_name='实际利润', default=0)
    isActive = models.BooleanField(default=True, verbose_name='状态')
    def __str__(self):
        return str(self.customerName)
    def to_dict(self):
        dic={}
        dic['id'] = self.id
        # 接单时间
        dic['startTime'] = self.startTime
        # 客户来源
        dic['tel'] = self.orderName
        dic['customerName'] = self.customerName
        # 客户单位
        dic['unit_name'] = self.customerUnit
        # 客户税号
        dic['unit_pwd'] = self.customerPwd
        # 要求
        dic['explain'] = self.explain
        # 数量
        dic['count'] = self.count
        # 未打完
        dic['notComple'] = self.notComple
        # 开票员
        dic['source'] = self.sourceName
        # 截止时间
        dic['endTime'] = self.endTime
        # 发票类型
        dic['style'] = self.style
        # 状态
        dic['status'] = self.status
        # 拿取方式
        dic['Delivery'] = self.Delivery
        # 地址
        dic['address'] = self.customerAddress
        # 点子
        dic['uTax'] = self.uTax
        # 应收
        dic['recivable'] = self.recivable
        # 实收
        dic['netReceiots'] = self.netReceiots
        # 预计成本
        dic['estimateCost'] = self.estimateCost
        # 实际成本
        dic['actualCost'] = self.actualCost
        # 预计利润
        dic['estimatProfit'] = self.estimatProfit
        # 实际利润
        dic['actualProfit'] = self.actualProfit
        return dic

    class Meta:
        app_label='order'
        verbose_name = '订单总表'
        verbose_name_plural = verbose_name