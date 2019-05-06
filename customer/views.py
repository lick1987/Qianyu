from django.urls import reverse

from customer.models import userCusterData
from index.views import *
from django.shortcuts import render
from index.models import *
from customer.models import *
#客户首页视图
def customer_view(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    userCust=userCusterData.objects.filter(user=id,isActive=1)
    return render(request,'customer.html',locals())

#修改客户
def modifyCuster(request,id=None):
    if request.method == 'GET':
        custMess = customer.objects.get(id=id)
        id = request.session.get('id')
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        return render(request,'modifyCustomer.html',locals())
    if request.method=='POST':
        uphone = request.POST.get('uphone', None)
        uwei = request.POST.get('uwei', None)
        uqq = request.POST.get('uqq', None)
        uname = request.POST.get('uname', None)
        uaddres = request.POST.get('uaddres', None)
        # uchoice = request.POST.get('uchoice', None)
        # uTax = request.POST.get('uTax', None)
        au = customer.objects.get(id=id)
        au.uphone = uphone
        au.uwei = uwei
        au.uqq = uqq
        au.uname = uname
        au.uaddres = uaddres
        # au.uchoice = uchoice
        # au.uTax = uTax
        au.save()
        return  HttpResponseRedirect('/customer')
#增加客户
def addCuster_views(request):
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
        # uTax = request.POST.get('uTax', None)
        #查询是否存在
        getName = customer.objects.filter(uphone=uphone,uwei=uwei,uqq=uqq,uname=uname,uaddres=uaddres)
        if not getName:
            dic = {
                'uphone': uphone,
                'uwei': uwei,
                'uqq': uqq,
                'uname': uname,
                'uaddres': uaddres,
            }
            customer(**dic).save()
        #获取新增客户ID
        custID=customer.objects.get(uphone=uphone,uwei=uwei,uqq=uqq,uname=uname,uaddres=uaddres,isActive=1)
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
            print(dic)
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

#删除客户
def deletCuster_views(request,id):
    userCust=userCusterData.objects.filter(id=id)
    if userCust:
        userCust[0].isActive=0
        userCust[0].save()
    return  HttpResponseRedirect('/customer')