import re
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
    day=int(time.strftime('%d', time.localtime(time.time())))
    monthList=list(range(1,13))
    yearList=list(range(2019,2030))
    # 只显示当前月份的所有信息

    userMes=[]
    for i in userCust:
        if getTime in i.startTime:
            userMes.append(i)
    userCust=userMes
    #获取剩余的
    for i in userCust:
        total = orderDate.objects.filter(user=id,order=i)
        #已打金额
        totalNumber=0
        if total:
            s=total[0].saveNumber.split(',')
            for index,j in enumerate(s):
                if index<5*day:
                    if j:
                        totalNumber+=int(j)
            #剩余金额
            s1=int(i.count)-totalNumber
            if s1!=int(i.notComple):
                i.notComple=s1
                i.save()


    #获取总共数量等
    #应收数量
    recivable=0
    netReceiots=0
    estimateCost=0
    actualCost=0
    estimatProfit=0
    actualProfit=0
    for i in userCust:
        recivable+=i.recivable
        netReceiots+=i.netReceiots
        estimatProfit+=i.estimatProfit
        actualProfit+=i.actualProfit
        estimatProfit+=i.estimatProfit
        actualProfit+=i.actualProfit
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
def modifyOrder(request,getId=None):
    if request.method == 'GET':
        id = request.session.get('id')
        sourceMes = userSourceData.objects.filter(user=id, isActive=1)
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        if int(getId)!=0:
            orderMes = order.objects.get(id=getId)
            return render(request,'modifyOrder.html',locals())
        else:
            getTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            orderMes={
                'id':0,
                'notComple':0,
                'netReceiots':0,
                'actualCost':0,
                'uTax':4,
                'count':0,
                'startTime':getTime,
                'endTime':getTime,
            }
            return render(request,'modifyOrder.html',locals())
    if request.method=='POST':
        id=request.session.get('id')
        user1=user.objects.get(id=id)
        userId = user.objects.filter(id=id)
        order_orderName = request.POST.get('order_orderName', None)
        order_startTime = request.POST.get('order_startTime', None)
        order_customerName = request.POST.get('order_customerName', None)
        order_customerUnit = request.POST.get('order_customerUnit', None)
        order_customerPwd = request.POST.get('order_customerPwd', None)
        order_explain = request.POST.get('order_explain', None)
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

        #增加订单
        if int(getId)!=0:
            au = order.objects.get(id=getId)

            au.orderName=order_orderName
            au.startTime=order_startTime
            au.customerName=order_customerName
            au.customerUnit=order_customerUnit
            au.customerPwd=order_customerPwd
            au.sourceName=order_source
            au.explain=order_explain
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
            if order_actualCost:
                #如果输入实收
                if int(order_netReceiots):
                    au.actualProfit =int(order_netReceiots)-int(order_actualCost)
                else:
                    #实际利润
                    au.actualProfit=int(order_count)*int(order_uTax)/100.0-int(order_netReceiots)
            else:
                #如果输入了实收
                if order_netReceiots:
                    au.actualProfit=int(order_netReceiots)-au.estimateCost
                else:
                    au.actualProfit=estimatProfit
            au.save()

            #如果单位不存在就保存在单位数据库
            # 查询是否存在
            getName = unit.objects.filter(uname=order_customerUnit, upwd=order_customerPwd)
            if not getName:
                dic = {
                    'upwd': order_customerPwd,
                    'uname': order_customerUnit,
                }
                unit(**dic).save()
            # 获取新增单位ID
            unitID = unit.objects.get(uname=order_customerUnit, upwd=order_customerPwd)
            # 查询表里面是否存在
            result = allData.objects.filter(user=userId[0], unit=unitID, isActive=1)
            status = 0
            if result:
                pass
            else:
                result = allData.objects.filter(user=userId[0], unit=unitID, isActive=0)
                if result:
                    result[0].isActive = 1
                    result[0].save()
                else:
                    dic = {
                        'user': userId[0],
                        'unit': unitID
                    }
                    allData(**dic).save()

            return  HttpResponseRedirect('/order')
        #修改订单
        else:
            if int(order_actualCost):
                #如果输入实收
                if order_netReceiots:
                    actualProfit =int(order_netReceiots)-int(order_actualCost)
                else:
                    #实际利润
                    actualProfit=int(order_count)*int(order_uTax)/100.0-int(order_netReceiots)
            else:
                #如果输入了实收
                if int(order_netReceiots):
                    actualProfit=int(order_netReceiots)-int(order_count)*0.03
                else:
                    actualProfit=int(order_count)*int(order_uTax)/100.0-int(order_count)*0.03
            dic={
                'user':user1,
                'orderName':order_orderName,
                'startTime':order_startTime,
                'customerName':order_customerName,
                'customerUnit':order_customerUnit,
                'customerPwd':order_customerPwd,
                'explain':order_explain,
                'sourceName':order_source,
                'count':order_count,
                'notComple' :order_notComple,
                'endTime' :order_endTime,
                'style' : order_style,
                'status':  order_status,
                'Delivery':order_Delivery,
                'customerAddress':order_customerAddress,
                'uTax':order_uTax,
                # 应收
                'recivable':(int(order_count) * int(order_uTax) / 100.0),
                'netReceiots': int(order_netReceiots),
                # 预计成本
                'estimateCost':(int(order_count) * 0.03),
                # 实际成本
                'actualCost':order_actualCost,
                # 预计利润
                'estimatProfit':(int(order_count) * int(order_uTax) / 100.0 - int(order_count) * 0.03),
                'actualProfit':int(actualProfit)
            }
            order(**dic).save()
            # 如果单位不存在就保存在单位数据库
            # 查询是否存在
            getName = unit.objects.filter(uname=order_customerUnit, upwd=order_customerPwd)
            if not getName:
                dic = {
                    'upwd': order_customerPwd,
                    'uname': order_customerUnit,
                }
                unit(**dic).save()
            # 获取新增单位ID
            unitID = unit.objects.get(uname=order_customerUnit, upwd=order_customerPwd)
            # 查询表里面是否存在
            result = allData.objects.filter(user=userId[0], unit=unitID, isActive=1)
            status = 0
            if result:
                pass
            else:
                result = allData.objects.filter(user=userId[0], unit=unitID, isActive=0)
                if result:
                    result[0].isActive = 1
                    result[0].save()
                else:
                    dic = {
                        'user': userId[0],
                        'unit': unitID
                    }
                    allData(**dic).save()
            return HttpResponseRedirect('/order')
def get_Customer(request):
    order_customerName = request.GET.get('order_customerName', None)
    customer1=customer.objects.filter(uwei__contains=order_customerName)
    customer1 = serializers.serialize('json', customer1)
    return HttpResponse(customer1)
def get_Unit(request):
    order_customerUnit = request.GET.get('order_customerUnit', None)
    customerUnit=unit.objects.filter(uname__contains=order_customerUnit)
    customerUnit1 = serializers.serialize('json', customerUnit)
    return HttpResponse(customerUnit1)
#预期安排
def orderDate_views(request,getid):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    oDate = orderDate.objects.filter(order=int(getid))
    DList = {}
    if oDate:
        oDate=oDate[0]
        dateList=oDate.saveNumber.split(',')
        for index,i in enumerate(dateList):
            try:
                DList['d%d'%index]=int(i)
            except:
                DList['d%d' % index] = ''
    else:
        for i in range(155):
            DList['d%d'%i]=''
    return render(request,'orderDate.html',locals())
def changeOrderDate_views(request):
    getId=request.GET.get('id')
    totalStr=request.GET.get('total')[:-1]
    id = request.session.get('id')
    print(totalStr)
    user1=user.objects.get(id=id)
    order1=order.objects.get(id=getId)
    orderDate1=orderDate.objects.filter(user=user1,order=order1)
    if orderDate1:
        orderDate1[0].saveNumber=totalStr
        orderDate1[0].save()
    else:
        dic={
            'user':user1,
            'order':order1,
            'saveNumber':totalStr
        }
        orderDate(**dic).save()
    return  HttpResponse(json.dumps('修改成功'))
#删除客户
def deletOrder_views(request,id):
    userCust=order.objects.filter(id=id)
    if userCust:
        userCust[0].isActive=0
        userCust[0].save()
    return  HttpResponseRedirect('/order')