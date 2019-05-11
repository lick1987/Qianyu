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
        dic={}
        if startTime in i.startTime:
            dic['id']=i.id
            #接单时间
            dic['startTime']=i.startTime
            #客户来源
            dic['tel']=i.customer.uname
            #客户微信或者QQ
            if i.customer.uwei:
                dic['customerName']=i.customer.uwei
            else:
                dic['customerName'] = i.customer.uqq
            #客户单位
            dic['unit_name']=i.unit.uname
            #客户税号
            dic['unit_pwd']=i.unit.upwd
            #要求
            dic['explain']=i.explain
            #数量
            dic['count']=i.count
            #未打完
            dic['notComple']=i.notComple
            #开票员
            dic['source']=i.source.uname
            #截止时间
            dic['endTime']=i.endTime
            #发票类型
            dic['style']=i.style
            #状态
            dic['status']=i.status
            #拿取方式
            dic['Delivery']=i.Delivery
            #地址
            dic['address']=i.customer.uaddres
            #点子
            dic['uTax']=i.uTax
            #应收
            dic['recivable']=i.recivable
            #实收
            dic['netReceiots']=i.netReceiots
            #预计成本
            dic['estimateCost']=i.estimateCost
            #实际成本
            dic['actualCost']=i.actualCost
            #预计利润
            dic['estimatProfit']=i.estimatProfit
            #实际利润
            dic['actualProfit']=i.actualProfit
            userList.append(dic)
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
        count = request.POST.get('order_count', None)
        startTime = request.POST.get('order_startTime', None)
        endTime = request.POST.get('order_endTime', None)
        status = request.POST.get('order_uchoice', None)
        uTax = request.POST.get('order_uTax', None)
        explain = request.POST.get('order_explain', None)
        sourceName = request.POST.get('order_source', None)
        style = request.POST.get('order_style', None)
        sourceMes = source.objects.filter(uname=sourceName)
        # customer1 = customer.objects.filter()
        au = order.objects.get(id=id)

        au.count = count
        au.startTime = startTime
        au.endTime = endTime
        au.status = status
        au.uTax = uTax
        au.style = style
        au.source = sourceMes[0]
        au.explain = explain
        au.save()
        return  HttpResponseRedirect('/order')
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