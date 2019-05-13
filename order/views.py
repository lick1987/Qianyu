import time

from django.core import serializers
from django.urls import reverse

from customer.models import userCusterData
from index.views import *
from django.shortcuts import render
from index.models import *
from customer.models import *
from order.models import *
from source.models import *
#客户首页视图显示当前月份信息
def order_view(request):
    id = request.session.get('id')
    dic = {
        '0': '未安排',
        '1': '已安排',
        '2': '待寄出',
        '3': '待付款',
        '4': '已完结',

    }
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    userCust=order.objects.filter(user=id,isActive=1)
    # 获取当前月份和年份
    getTime = time.strftime('%Y-%m', time.localtime(time.time()))
    month=int(time.strftime('%m', time.localtime(time.time())))
    year=int(time.strftime('%Y', time.localtime(time.time())))
    monthList=list(range(1,13))
    yearList=list(range(2019,2030))
    # 只显示当前月份的所有信息
    userMes=[]
    for i in userCust:
        if getTime in i.startTime:
            userMes.append(i)
    userCust=userMes
    return render(request,'order.html',locals())
#获取状态信息用于状态颜色显示
def get_status(request):
    id = request.session.get('id')
    userCust = order.objects.filter(user=id, isActive=1)
    userCust1 = serializers.serialize('json', userCust)
    return HttpResponse(userCust1)
#status1状态显示
def status_views(request,status):
    id = request.session.get('id')
    dic={
        '0':'未安排',
        '1':'已安排',
        '2':'待寄出',
        '3':'待付款',
        '4':'已完结'
    }
    # status = request.GET.get('status', None)
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    status1=dic[status]
    userCust = order.objects.filter(user=id, isActive=1,status=status1)
    userCust1=serializers.serialize('json',userCust)
    return render(request,'order.html',locals())
#改变显示信息
def change_show(request):
    id = request.session.get('id')
    status = request.GET.get('status', None)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    startTime='%s-%02d'%(year,int(month))
    if status=='所有状态':
        userCust = order.objects.filter(user=id, isActive=1)
    else:
        userCust = order.objects.filter(user=id, isActive=1, status=status)
    userList=[]
    for i in userCust:
        if startTime in i.startTime:
            s=i.to_dict()
            userList.append(s)
    return HttpResponse(json.dumps(userList))
#修改订单
def modifyOrder(request,id=None):
    if request.method == 'GET':
        orderMes = order.objects.get(id=id)
        id = request.session.get('id')
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        sourceMes = userSourceData.objects.filter(user=id, isActive=1)
        return render(request,'modifyOrder.html',locals())
    if request.method=='POST':
        order_orderName = request.POST.get('order_orderName', None)
        order_startTime = request.POST.get('order_startTime', None)
        order_customerName = request.POST.get('order_customerName', None)
        order_customerUnit = request.POST.get('order_customerUnit', None)
        order_customerPwd = request.POST.get('order_customerPwd', None)
        order_source = request.POST.get('order_sourceName', None)
        #订购数量
        order_count = request.POST.get('order_count', None)
        #未完成
        order_notComple = request.POST.get('order_notComple', None)
        order_endTime = request.POST.get('order_endTime', None)
        order_style = request.POST.get('order_style', None)
        #
        order_status = request.POST.get('order_status', None)
        order_Delivery = request.POST.get('order_Delivery', None)
        order_customerAddress = request.POST.get('order_customerAddress', None)
        #点子
        order_uTax = request.POST.get('order_uTax', None)
        #
        # order_recivable = request.POST.get('order_recivable', None)
        order_netReceiots = request.POST.get('order_netReceiots', None)
        # order_estimateCost = request.POST.get('order_estimateCost', None)
        order_actualCost = request.POST.get('order_actualCost', None)
        # order_estimatProfit = request.POST.get('order_estimatProfit', None)
        # order_actualProfit = request.POST.get('order_actualProfit', None)
        au = order.objects.get(id=id)
        au.orderName=order_orderName
        au.startTime=order_startTime
        au.customerName=order_customerName
        au.customerUnit=order_customerUnit
        au.customerPwd=order_customerPwd
        au.sourceName=order_source
        au.count=order_count
        au.notComple=order_notComple
        au.endTime=order_endTime
        au.style=order_style
        au.status=order_status
        au.Delivery=order_Delivery
        au.customerAddress=order_customerAddress
        au.uTax=order_uTax
        #应收
        recivable=int(order_count)*int(order_uTax)/100.0
        au.recivable=recivable
        au.netReceiots=order_netReceiots
        #预计成本
        au.estimateCost=int(order_count)*0.03
        #实际成本
        au.actualCost=order_actualCost
        #预计利润
        estimatProfit=int(order_count)*int(order_uTax)/100.0-int(order_count)*0.03
        au.estimatProfit=estimatProfit
        #如果输入实际成本
        if int(order_actualCost):
            #如果输入实收
            if int(order_netReceiots):
                au.actualProfit =int(order_netReceiots)-int(order_actualCost)
            else:
                #实际利润
                au.actualProfit=int(order_count)*int(order_uTax)/100.0-int(order_netReceiots)
        else:
            #如果输入了实收
            if int(order_netReceiots):
                au.actualProfit=int(order_netReceiots)-au.estimateCost
            else:
                au.actualProfit=estimatProfit
        au.save()
        return  HttpResponseRedirect('/order')
def get_Customer(request):
    order_customerName = request.GET.get('order_customerName', None)
    customer1=customer.objects.filter(uwei__contains=order_customerName)
    customer1 = serializers.serialize('json', customer1)
    return HttpResponse(customer1)
#增加客户
def addOrder_views(request):
    if request.method == "GET":
        id = request.session.get('id')
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        return render(request,'addCustomer.html',locals())
    #提交增加客户
    elif request.method=="POST":
        id=request.session['id']
        userId=user.objects.filter(id=id)
        uphone = request.POST.get('uphone', None)
        uwei = request.POST.get('uwei', None)
        uqq = request.POST.get('uqq', None)
        uname = request.POST.get('uname', None)
        uaddres = request.POST.get('uaddres', None)
        # uchoice = request.POST.get('uchoice', None)
        uTax = request.POST.get('uTax', None)
        #查询是否存在
        getName = customer.objects.filter(uphone=uphone,uwei=uwei,uqq=uqq,uname=uname)
        if not getName:
            dic = {
                'uphone': uphone,
                'uwei': uwei,
                'uqq': uqq,
                'uname': uname,
                'uaddres': uaddres,
                # 'uchoice': uchoice,
                'uTax': uTax,
            }
            customer(**dic).save()
        #获取新增单位ID
        custID=customer.objects.get(uphone=uphone,uwei=uwei,uqq=uqq,uname=uname)
        #查询表里面是否存在
        result=userCusterData.objects.filter(user=userId[0],customer=custID,isActive=1)
        status=0
        if  result:
            status=1
            dic = {
                'status': status,
                'message': '客户已经存在'

            }
            resp = HttpResponse(json.dumps(dic))
        #没有则保存
        else:
            result=userCusterData.objects.filter(user=userId[0],customer=custID,isActive=0)
            if result:
                result[0].isActive=1
                result[0].save()
            else:
                dic={
                    'user':userId[0],
                    'customer':custID
                }
                userCusterData(**dic).save()
            dic = {
                'status': status,
                'message': '客户添加成功'
            }
            resp = HttpResponse(json.dumps(dic))
        return resp
    pass

#删除客户
def deletOrder_views(request,id):
    userCust=userCusterData.objects.filter(id=id)
    if userCust:
        userCust[0].isActive=0
        userCust[0].save()
    return  HttpResponseRedirect('/customer')