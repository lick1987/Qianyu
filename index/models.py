from django.db import models
#声明自定义objects类-AuthorManager继承自models.Manager
class countManager(models.Manager):
    #添加自定义函数查询表中共有多少条数据
    def auCount(self):
        return self.all().count()
    def auCount1(self,n):
        return self.filter(age__gte=n)

#单位表
class unit(models.Model):
    uname = models.CharField(max_length=50,verbose_name='单位名称')
    upwd = models.CharField(max_length=50,verbose_name='单位税号')
    isActive = models.BooleanField(default=True, verbose_name='状态')
    def __str__(self):
        return str(self.uname)
    class Meta:
        verbose_name = '单位信息'
        verbose_name_plural = verbose_name
#客户表
class customer(models.Model):
    uphone = models.CharField(max_length=11,verbose_name='手机号')
    uwei = models.CharField(max_length=20,verbose_name='微信')
    uqq = models.CharField(max_length=15,verbose_name='QQ')
    uname = models.CharField(max_length=20,verbose_name='用户名')
    uaddres=models.CharField(max_length=200,verbose_name='收货地址')
    uchoice=models.CharField(max_length=10,verbose_name='发票类型',default='纸质发票')
    uTax=models.CharField(max_length=10,verbose_name='发票点子',default='4')
    isActive = models.BooleanField(default=True,verbose_name='状态')
    unit=models.ManyToManyField(unit)
    def __str__(self):
        return str(self.uname)
    class Meta:
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name

#用户表
class user(models.Model):
    uname = models.CharField(max_length=11,verbose_name='账号')
    upwd = models.CharField(max_length=20,verbose_name='密码')
    #用于找回密码
    uemail=models.EmailField(max_length=30,verbose_name='邮箱',default=None)
    #用户和客户多对多
    customer=models.ManyToManyField(customer)
    isActive = models.BooleanField(default=True,verbose_name='状态')
    def __str__(self):
        return str(self.uname)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
#查询单位总表
class allData(models.Model):
    user=models.ForeignKey(user,True)
    unit=models.ForeignKey(unit,True)
    isActive = models.BooleanField(default=True, verbose_name='状态')

    def __str__(self):
        return str(self.unit)
    class Meta:
        verbose_name = '总表'
        verbose_name_plural = verbose_name
        ordering = ['unit']
#订单总表
# class order(models.Model):
#     status_choice  = (
#         (0, '未安排'),
#         (1, '已安排'),
#         (2, '待寄出'),
#         (3, '待付款'),
#         (4, '已完结')
#     )
#     user=models.ForeignKey(user,True)
#     customer=models.ForeignKey(customer,True)
#     unit=models.ForeignKey(unit,True)
#     count=models.CharField(max_length=100,verbose_name='数量')
#     #状态
#     isActive = models.BooleanField(default=0, verbose_name='状态',choices=status_choice)
#     #接单时间
#     startTime = models.DateTimeField(auto_now_add=True,verbose_name='接单时间')
#     #完结时间
#     endTime=models.DateTimeField(verbose_name='预期完结时间')
#     def __str__(self):
#         return str(self.customer)
#
#     class Meta:
#         verbose_name = '订单总表'
#         verbose_name_plural = verbose_name