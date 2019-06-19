import random
import re
import time

import xlwt
from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.urls import reverse

from customer.models import userCusterData
from index.views import *
from django.shortcuts import render
from index.models import *
from customer.models import *
from lib.FileTool.base import handle_uploaded_file
from order.forms import UploadFileForm
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
        '5': '未完成',

    }
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    userCust=order.objects.filter(user=id,isActive=1).order_by('-startTime','customerName')
    # 获取当前月份和年份
    getTime = time.strftime('%Y-%m', time.localtime(time.time()))
    month=float(time.strftime('%m', time.localtime(time.time())))
    year=float(time.strftime('%Y', time.localtime(time.time())))
    day=float(time.strftime('%d', time.localtime(time.time())))
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
                if index<=5*day:
                    if j:
                        totalNumber+=float(j)
            #剩余金额
            s1=float(i.count)-totalNumber
            if s1!=float(i.notComple):
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
    totalCount=0
    notComple=0
    for i in userCust:
        recivable+=float(i.recivable)
        netReceiots+=float(i.netReceiots)
        estimateCost+=float(i.estimateCost)
        actualCost+=float(i.actualCost)
        estimatProfit+=float(i.estimatProfit)
        actualProfit+=float(i.actualProfit)
        totalCount+=float(i.count)
        if i.notComple:
            notComple+=float(i.notComple)
    bfb="%s"%int(notComple/totalCount*100)+'%'
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
        '4':'已完结',
        '5':'未完成'
    }
    # status = request.GET.get('status', None)
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    status1=dic[status]
    if status1=='未完成':
        userCust = order.objects.filter(~Q(status=dic[4]),user=id, isActive=1).order_by('-startTime','customerName')
    else:
        userCust = order.objects.filter(user=id, isActive=1,status=status1).order_by('-startTime','customerName')
    userCust1=serializers.serialize('json',userCust)
    return render(request,'order.html',locals())
#改变显示信息
def change_show(request):
    id = request.session.get('id')
    status = request.GET.get('status', None)
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    search = request.GET.get('search', None)
    if float(month)==13:
        startTime=''
    else:
        startTime = '%s-%02d' % (year, float(month))
    #有搜索需求
    if search:
        startTime = '%s-%02d' % (year, float(month))
        if status == '所有状态':
            userCust = order.objects.filter(user=id, isActive=1).order_by('-startTime','customerName')
        elif status == '未完成':
            userCust = order.objects.filter(~Q(status='已完结'), user=id, isActive=1).order_by('-startTime','customerName')
            userList = []
            for i in userCust:
                s = i.to_dict()
                if search in str(s):
                    userList.append(s)
            return HttpResponse(json.dumps(userList))
        else:
            userCust = order.objects.filter(user=id, isActive=1, status=status).order_by('-startTime','customerName')
        userList = []
        for i in userCust:
            if startTime in i.startTime:
                s = i.to_dict()
                if search in str(s):
                    userList.append(s)
        return HttpResponse(json.dumps(userList))
    else:
        if status=='所有状态':
            userCust = order.objects.filter(user=id, isActive=1).order_by('-startTime','customerName')
        elif status=='未完成':
            userCust = order.objects.filter(~Q(status='已完结'), user=id, isActive=1).order_by('-startTime','customerName')
            userList = []
            for i in userCust:
                s = i.to_dict()
                userList.append(s)
            return HttpResponse(json.dumps(userList))
        else:
            userCust = order.objects.filter(user=id, isActive=1, status=status).order_by('-startTime','customerName')
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
        if float(getId)!=0:
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

        #修改订单
        if float(getId)!=0:
            au = order.objects.get(id=getId)
            au.orderName=order_orderName
            au.startTime=order_startTime
            au.customerName=order_customerName
            au.customerUnit=order_customerUnit
            au.customerPwd=order_customerPwd
            au.sourceName=order_source
            au.explain=order_explain
            au.count=order_count
            au.endTime=order_endTime
            au.style=order_style
            au.status=order_status
            au.Delivery=order_Delivery
            au.customerAddress=order_customerAddress
            au.uTax=order_uTax
            #应收
            recivable=float(order_count)*float(order_uTax)/100.0
            au.recivable=recivable
            au.netReceiots=order_netReceiots
            #预计成本
            au.estimateCost=float(order_count)*0.03
            #实际成本
            au.actualCost=order_actualCost
            #预计利润
            estimatProfit=float(order_count)*float(order_uTax)/100.0-float(order_count)*0.03
            au.estimatProfit=estimatProfit
            #如果输入实际成本
            if float(order_actualCost):
                #如果输入实收
                if float(order_netReceiots):
                    au.actualProfit =float(order_netReceiots)-float(order_actualCost)
                else:
                    #实际利润
                    au.actualProfit=float(order_count)*float(order_uTax)/100.0-float(order_netReceiots)
            else:
                #如果输入了实收
                if float(order_netReceiots):
                    au.actualProfit=float(order_netReceiots)-au.estimateCost
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
        #增加订单
        else:
            #如果输入实际成本
            if float(order_actualCost):
                #如果输入实收
                if float(order_netReceiots):
                    actualProfit =float(order_netReceiots)-float(order_actualCost)
                else:
                    #实际利润
                    actualProfit=float(order_count)*float(order_uTax)/100.0-float(order_netReceiots)
            else:
                #如果输入了实收
                if float(order_netReceiots):
                    actualProfit=float(order_netReceiots)-float(order_count)*0.03
                else:
                    actualProfit=float(order_count)*float(order_uTax)/100.0-float(order_count)*0.03

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
                'endTime' :order_endTime,
                'style' : order_style,
                'status':  order_status,
                'Delivery':order_Delivery,
                'customerAddress':order_customerAddress,
                'notComple':order_count,
                'uTax':order_uTax,
                # 应收
                'recivable':(float(order_count) * float(order_uTax) / 100.0),
                'netReceiots': float(order_netReceiots),
                # 预计成本
                'estimateCost':(float(order_count) * 0.03),
                # 实际成本
                'actualCost':order_actualCost,
                # 预计利润
                'estimatProfit':(float(order_count) * float(order_uTax) / 100.0 - float(order_count) * 0.03),
                'actualProfit':float(actualProfit)
            }
            order_List=order.objects.filter(**dic)
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
#上传图片
def upload_views(request,getId):
    id = request.session.get('id')

    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES) # 注意获取数据的方式
        if form.is_valid():
            f=request.FILES['file']
            title=request.POST.get('title',None)
            imgName=re.sub(r'[\s\S]*\.','%s.'%title,f.name)
            r1 = random.randint(0, 1000)
            r2 = random.randint(0, 1000)
            r3 = random.randint(0, 1000)
            r4 = random.randint(0, 1000)
            r5 = random.randint(0, 1000)
            r6 = random.randint(0, 1000)
            r = str(r1) + str(r2) + str(r3) + str(r4) + str(r6)
            imgName='%s%s'%(r,imgName)
            url = settings.STATICFILES_DIRS[0]+'\index\static\\upload\%s'%imgName
            handle_uploaded_file(f,url)
            #保存进数据库
            user1=user.objects.get(id=id)
            order1=order.objects.get(id=getId)
            imgs = img.objects.filter(user=user1,order=order1,filePath='/static/upload/%s'%imgName)
            dic={
                'user':user1,
                'order':order1,
                'filePath':'/static/upload/%s'%imgName,
                'isActive':True,
                'title':title
            }
            img(**dic).save()
            imgs = img.objects.filter(order=getId, isActive=1)
    else:
        form = UploadFileForm()
        imgs=img.objects.filter(order=getId,isActive=1)
    return render(request, 'upload.html', locals())
#预期安排
def orderDate_views(request,getid):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    oDate = orderDate.objects.filter(order=float(getid))
    DList = {}
    if oDate:
        oDate=oDate[0]
        dateList=oDate.saveNumber.split(',')
        for index,i in enumerate(dateList):
            try:
                DList['d%d'%index]=float(i)
            except:
                DList['d%d' % index] = ''
            # if DList['d%d'%index]:
            #     getTime = time.strftime('%Y-%m', time.localtime(time.time()))
            #
    else:
        for i in range(155):
            DList['d%d'%i]=''
    return render(request,'orderDate.html',locals())
def changeOrderDate_views(request):
    getId=request.GET.get('id')
    totalStr=request.GET.get('total')[:-1]
    id = request.session.get('id')
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


#再次下单
def againOrder_views(request,getId):
    id = request.session.get('id')
    user1 = user.objects.get(id=id)
    getTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    orderMes = order.objects.get(id=getId)
    mesDic=orderMes.to_dict1()
    mesDic['startTime']=getTime
    mesDic['status']='未安排'
    mesDic['recivable'] = 0
    mesDic['notComple'] = '0'
    mesDic['user'] =user1
    # 实收
    mesDic['netReceiots'] = 0
    # 预计成本
    mesDic['estimateCost'] = 0
    # 实际成本
    mesDic['actualCost'] = 0
    # 预计利润
    mesDic['estimatProfit'] = 0
    # 实际利润
    mesDic['actualProfit'] = 0
    mesDic['count'] =0
    order(**mesDic).save()
    id1=order.objects.filter(user=user1).order_by('-id')[0]
    order1=order.objects.filter(user=user1,id=getId)
    imgMes1 = img.objects.filter(user=user1, order=order1[0],isActive=1)
    for imgMes in imgMes1:
        dic={
            'title':imgMes.title,
            'user':user1,
            'order':id1,
            'filePath':imgMes.filePath
        }
        img(**dic).save()
    return HttpResponseRedirect('/order')
def deltUpload_views(request,getId):
    IMG=img.objects.filter(id=getId)[0]
    IMG.isActive=0
    IMG.save()
    orderId=IMG.order.id
    return HttpResponseRedirect('/order/upload/%s'%orderId)
    # return HttpResponseRedirect(‘)
def saveOrder_views(request):
    getTime = time.strftime('%Y-%m', time.localtime(time.time()))
    id = request.session.get('id')
    user1 = user.objects.get(id=id)
    # 打开文件
    workbook = xlwt.Workbook(encoding='utf-8')
    # 获取所有sheet
    # 创建一个worksheet
    worksheet = workbook.add_sheet('getTime')
    # 写入excel
    # 参数对应 行, 列, 值
    exList = ['接单时间', '接单账号', '客户姓名', '抬头', '要求', '数量',
              '未打完', '开票员', '截止日期', '发票类型', '状态', '拿取方式',
              '地址', '点子', '应收', '实收', '预计成本', '实际成本', '预计利润', '实际利润']
    for index, i in enumerate(exList):
        worksheet.write(0, index, label=i)
    order1 = order.objects.filter(user=user1,isActive=1).order_by('startTime')
    for index,orders in enumerate(order1):
        worksheet.write(index+1,0,label=orders.startTime)
        worksheet.write(index+1,1,label=orders.orderName)
        worksheet.write(index+1,2,label=orders.customerName)
        worksheet.write(index+1,3,label=orders.customerUnit+'\n'+orders.customerPwd)
        worksheet.write(index+1,4,label=orders.explain)
        worksheet.write(index+1,5,label=orders.count)
        worksheet.write(index+1,6,label=orders.notComple)
        worksheet.write(index+1,7,label=orders.sourceName)
        worksheet.write(index+1,8,label=orders.endTime)
        worksheet.write(index+1,9,label=orders.style)
        worksheet.write(index+1,10,label=orders.status)
        worksheet.write(index+1,11,label=orders.Delivery)
        worksheet.write(index+1,12,label=orders.customerAddress)
        worksheet.write(index+1,13,label=orders.uTax)
        worksheet.write(index+1,14,label=orders.recivable)
        worksheet.write(index+1,15,label=orders.netReceiots)
        worksheet.write(index+1,16,label=orders.estimateCost)
        worksheet.write(index+1,17,label=orders.actualCost)
        worksheet.write(index+1,18,label=orders.estimatProfit)
        worksheet.write(index+1,19,label=orders.actualProfit)
    url = settings.STATICFILES_DIRS[0] + '/index/static/excel/%s'+'.xls'
    workbook.save(url%getTime)
    return HttpResponseRedirect('/order')
#删除客户
def deletOrder_views(request,id):
    userCust=order.objects.filter(id=id)
    if userCust:
        userCust[0].isActive=0
        userCust[0].save()
    return  HttpResponseRedirect('/order')