from django.urls import reverse

from customer.models import userCusterData
from index.views import *
from django.shortcuts import render
from index.models import *
from .models import *
#加油员首页视图
def source_view(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    userSource=userSourceData.objects.filter(user=id,isActive=1)
    return render(request,'source.html',locals())

#修改加油员信息
def modifyCuster_view(request,id=None):
    if request.method == 'GET':
        sourceMess = source.objects.get(id=id)
        id = request.session.get('id')
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        return render(request,'modifySource.html',locals())
    if request.method=='POST':
        uphone = request.POST.get('source_uphone', None)
        uwei = request.POST.get('source_uwei', None)
        uqq = request.POST.get('source_uqq', None)
        uname = request.POST.get('source_uname', None)
        uaddres = request.POST.get('source_uaddres', None)
        # uchoice = request.POST.get('uchoice', None)
        uTax = request.POST.get('source_uTax', None)
        au = source.objects.get(id=id)
        au.uphone = uphone
        au.uwei = uwei
        au.uqq = uqq
        au.uname = uname
        au.uaddres = uaddres
        # au.uchoice = uchoice
        au.uTax = uTax
        au.save()
        return  HttpResponseRedirect('/source')
#增加加油员
def addSource_views(request):
    if request.method == "GET":
        id = request.session.get('id')
        flag = False
        if id:
            uname = request.session['uname']
            flag = True
        return render(request,'addSource.html',locals())
    #提交增加客户
    elif request.method=="POST":
        id=request.session['id']
        userId=user.objects.filter(id=id)
        uphone = request.POST.get('uphone', None)
        uwei = request.POST.get('uwei', None)
        uname = request.POST.get('uname', None)
        uaddres = request.POST.get('uaddres', None)
        # uchoice = request.POST.get('uchoice', None)
        uTax = request.POST.get('uTax', None)
        #查询是否存在
        getName = source.objects.filter(uphone=uphone,uwei=uwei,uname=uname)
        if not getName:
            dic = {
                'uphone': uphone,
                'uwei': uwei,
                'uname': uname,
                'uaddres': uaddres,
                # 'uchoice': uchoice,
                'uTax': uTax,
            }
            source(**dic).save()

        #获取新增单位ID
        sourceID=source.objects.get(uphone=uphone,uwei=uwei,uname=uname)
        #查询表里面是否存在
        result=userSourceData.objects.filter(user=userId[0],source=sourceID,isActive=1)
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
            result=userSourceData.objects.filter(user=userId[0],source=sourceID,isActive=0)
            if result:
                result[0].isActive=1
                result[0].save()
            else:
                dic={
                    'user':userId[0],
                    'source':sourceID
                }
                userSourceData(**dic).save()
            dic = {
                'status': status,
                'message': '客户添加成功'
            }
            resp = HttpResponse(json.dumps(dic))
        return resp
    pass

#删除加油员
def deletCuster_views(request,id):
    userCust=userSourceData.objects.filter(id=id)
    if userCust:
        userCust[0].isActive=0
        userCust[0].save()
    return  HttpResponseRedirect('/source')