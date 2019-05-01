import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
#首页视图
from .models import *

#检查登录状态
def check_login_views(request):
    if request.method == 'GET':
        #判断session中是否有对应的信息
        uname = request.session.get('uname', '')
        id = request.session.get('id', '')
        #如果有
        flag = False
        if uname and id:
            flag='true'
            return render(request,'qianduan.html',locals())
        #如果没有
        else:
            #如果cookie中有
            if 'id' in request.COOKIES and 'uname' in request.COOKIES:
                request.session['uname'] = request.COOKIES['uname']
                request.session['id'] = request.COOKIES['id']
                flag = 'true'
                return render(request, 'qianduan.html', locals())
            #如果没有就到登录页面
            else:

                return render(request, 'qianduan.html', locals())
        # 处理请求post请求
    else:
        uname = request.POST['uname']
        upwd = request.POST['upwd']
        issave=request.POST['isSaved']
        uList = user.objects.filter(uname=uname, upwd=upwd)
        flag=False
        # 登录成功
        if uList:
            flag=True
            request.session['uname'] = uname
            request.session['id'] = uList[0].id
            # 点击记住密码将登录信息保存进cookie
            if issave=='true':
                dic = {
                    'status': 1,
                    'message': '欢迎：' + uname
                }
                resp = HttpResponse(json.dumps(dic))
                resp.set_cookie('uname', uname, 60 * 60 * 24 * 365)
                resp.set_cookie('id', uList[0].id, 60 * 60 * 24 * 365)
                return resp
            else:
                dic = {
                    'status': 1,
                    'message': '欢迎：' + uname
                }
                resp = HttpResponse(json.dumps(dic))
                return resp
        # 登录失败
        else:
            print('登录失败')
            dic = {
                'status': 0,
                'message': '用户名或者密码错误'
            }
            resp = HttpResponse(json.dumps(dic))
            return resp
#

def index_views(request):
     return check_login_views(request)

#单位视图
def unit_views(request):
    #获取数据库中所有的单位信息
    id = request.session.get('id')
    # 如果有
    flag = False
    if id:
        uname = request.session.get('uname', '')
        flag = 'true'
    uList1=allData.objects.filter(user=id,isActive=1)
    l=[]
    #获取名字列表
    l1=[]
    for i in uList1:
        l.append(i.unit.uname)
    l.sort()
    uList=[]
    for i in l:
        for u in uList1:
            if u.unit.uname==i and u.unit.upwd not in l1:
                l1.append(u.unit.upwd)
                uList.append(u)
    return render(request,'danwei.html',locals())
#删除单位
def deleteUnit_views(request,id=None):
    #从数据库中完成删除操作将isactive置0
    id1 = request.session['id']
    #获取单位对象
    unitMess = allData.objects.get(user=id1,unit=id)
    #获取单位
    unitMess.isActive=0
    unitMess.save()
    return unit_views(request)
#修改单位
def modifyUnit_views(request,id=None):
    unitMess = unit.objects.get(id=id)
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session.get('uname', '')
        flag = 'true'
    return render(request,'modifyUnit.html',locals())
#编辑单位
def modifyUnit_views1(request):
    if request.method == 'POST':
        id = request.POST.get('id', None)
        name = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        au = unit.objects.get(id=id)
        au.uname=name
        au.upwd=upwd
        au.save()
        return unit_views(request)
#增加单位视图
def addUnit_view(request):
    if request.method == "GET":
        return render(request,'addUnit.html')
    elif request.method=="POST":
        id=request.session['id']
        userId=user.objects.filter(id=id)
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        print(uname)
        print(upwd)
        #查询是否存在
        getName = unit.objects.filter(uname=uname,upwd=upwd)
        if not getName:
            dic = {
                'upwd': upwd,
                'uname': uname,
            }
            unit(**dic).save()
        #获取新增单位ID
        unitID=unit.objects.get(uname=uname,upwd=upwd)
        #查询表里面是否存在
        result=allData.objects.filter(user=userId[0],unit=unitID,isActive=1)
        status=0
        if  result:
            status=1
            dic = {
                'status': status,
                'message': '单位已存在'

            }
            resp = HttpResponse(json.dumps(dic))
        #没有则保存
        else:
            result=allData.objects.filter(user=userId[0],unit=unitID,isActive=0)
            if result:
                result[0].isActive=1
                result[0].save()
            else:
                dic={
                    'user':userId[0],
                    'unit':unitID
                }
                allData(**dic).save()
            dic = {
                'status': status,
                'message': '添加成功'
            }
            resp = HttpResponse(json.dumps(dic))
        return resp
#用户注册
def register_view(request):
    #注册模式
    if request.method=="POST":
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        uemail = request.POST.get('uemail', None)
        dic = {
            'upwd': upwd,
            'uname': uname,
            'uemail': uemail,
        }
        user(**dic).save()
        resp='注册成功'
        resp+="<a href='/'>返回首页</a>"
        return HttpResponse(resp)
    elif request.method=="GET":
        return render(request,'register.html')
#检测用户名是否存在
def check_name_view(request):
    uname = request.GET['uname']
    uList = user.objects.filter(uname=uname)
    # 如果存在响应：{"status":1}
    if uList:
        s = 1
        msg = '用户已经存在'
    # 如果不存在响应：{"status":0}
    else:
        s = 0
        msg = '恭喜你可以注册'
    dic = {'status': s, 'msg': msg}
    return HttpResponse(json.dumps(dic))
#用户退出操作
def exit_view(request):
    del request.session['id']
    del request.session['uname']
    flag = False
    # 记录原地址
    url = request.META.get('HTTP_REFERER', '/')
    resp = HttpResponseRedirect(url,locals())
    if 'id' in request.COOKIES:
        resp.delete_cookie('id')
        resp.delete_cookie('uname')
    return resp
#客户管理视图
def customer_view(request):
    id = request.session.get('id')
    customerAll=customer.objects.fiter()
    return render(request,'customer.html',locals())