from django.core import serializers
from django.urls import reverse

from customer.models import userCusterData
from index.views import *
from django.shortcuts import render
from index.models import *
from customer.models import *
from order.models import *
from source.models import *
#客户首页视图
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
    s=json.dumps({'List':json.dumps(list(range(100)))})
    return render(request,'order.html',locals())
#获取状态信息
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
    status1=dic[status]
    userCust = order.objects.filter(user=id, isActive=1,status=status1)
    return render(request,'order.html',locals())

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