import json
import time

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from order.models import *
from tomorrow.models import tomorrow

def tomorrow1(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    getTime = time.strftime('%Y-%m', time.localtime(time.time()))

    return render(request, 'tomorrow.html', locals())
def tomorrow_views(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    getTime = time.strftime('%Y-%m', time.localtime(time.time()))
    day = int(time.strftime('%d', time.localtime(time.time())))
    orderList = order.objects.exclude(notComple='0').order_by('sourceName')
    tomorrowList=[]
    for orders in orderList:
        tomorrowDict={}
        if orders.user.id==int(id) and orders.isActive==True:
            if orders.notComple!=0:
                #同月份
                if getTime in orders.startTime:
                    oDate=orderDate.objects.filter(order=orders)
                    if oDate:
                        sNumber=oDate[0].saveNumber.split(',')
                        str1=''
                        for i in sNumber[5*day:5*day+5]:
                            if i:
                                str1+=i+','
                        if str1:
                            tomorrowDict['arrange']=str1[:-1]
                            tomorrowDict['times']=time.strftime('%Y-%m-%d', time.localtime(time.time()))
                            tomorrowDict['customerUnit']=orders.customerUnit
                            tomorrowDict['customerPwd']=orders.customerPwd
                            tomorrowDict['sourceName']=orders.sourceName
                            tomorrowDict['customerName']=orders.customerName
                            tomorrowDict['explain']=orders.explain
                            tomorrowList.append(tomorrowDict)
                            tomorrows=tomorrow.objects.filter(times=tomorrowDict['times'],customerName=orders.customerName,customerUnit=tomorrowDict['customerUnit'])
                            if tomorrows:
                                pass
                            else:
                                tomorrow(**tomorrowDict).save()
    tomorrowList=tomorrow.objects.filter(times=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    # total = orderDate.objects.filter(user=id, order=i)
    return render(request,'tomorrow.html',locals())
def tomorrow_all_views(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    tomorrowList = tomorrow.objects.all().order_by('-times')
    return render(request, 'alltomorrow.html', locals())
def changeSource_views(request):
    sourceName = request.GET.get('sourceName', None)
    tId = request.GET.get('Id', None)
    result=tomorrow.objects.filter(id=tId)[0]
    result.sourceName=sourceName
    result.save()
    return HttpResponse('修改成功')
def changeShow_views(request):
    search = request.GET.get('search', None)
    tomorrowList = tomorrow.objects.all().order_by('-times')
    tomList=[]
    for i in tomorrowList:
        s = i.to_dic()
        if search in str(s):
            tomList.append(s)
    return HttpResponse(json.dumps(tomList))