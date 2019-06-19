import json
import re
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
    orderList = order.objects.exclude(notComple='0').filter(isActive=True,user=id,startTime__icontains=getTime).order_by('sourceName')
    tomorrowList=[]
    for orders in orderList:
        tomorrowDict={}
        oDate=orderDate.objects.filter(order=orders)
        if oDate:
            sNumber=oDate[0].saveNumber.split(',')
            str1=''
            for i in sNumber[5*day:5*day+5]:
                if i:
                    str1+=i+','
            if re.search('\d+',str1):
                tomorrowDict['arrange']=str1[:-1]
                tomorrowDict['times']=getTime+'-%s'%(day+1)
                tomorrowDict['customerUnit']=orders.customerUnit
                tomorrowDict['customerPwd']=orders.customerPwd
                tomorrowDict['sourceName']=orders.sourceName
                tomorrowDict['customerName']=orders.customerName
                tomorrowDict['explain']=orders.explain
                tomorrowList.append(tomorrowDict)
    return render(request,'tomorrow.html',locals())
def tomorrow_all_views(request):
    id = request.session.get('id')
    flag = False
    if id:
        uname = request.session['uname']
        flag = True
    day=request.GET.get('search','')
    year_select=request.GET.get('year_select',time.strftime('%Y', time.localtime(time.time())))
    mouth_select=request.GET.get('mouth_select',time.strftime('%m', time.localtime(time.time())))
    if day=='':
        day=int(time.strftime('%d', time.localtime(time.time())))+1
    day=int(day)
    getTime = '%d-%02d'%(int(year_select),int(mouth_select))
    orderList = order.objects.filter(isActive=True, user=id, startTime__icontains=getTime).order_by('sourceName')
    tomorrowList = []
    day=day-1
    for orders in orderList:
        tomorrowDict={}
        oDate=orderDate.objects.filter(order=orders)
        if oDate:
            sNumber=oDate[0].saveNumber.split(',')
            str1=''
            for i in sNumber[5*day:5*day+5]:
                if i:
                    str1+=i+','
            if re.search('\d+',str1):
                tomorrowDict['id']=orders.id
                tomorrowDict['arrange']=str1[:-1]
                tomorrowDict['times']=getTime+'-%s'%(day+1)
                tomorrowDict['customerUnit']=orders.customerUnit
                tomorrowDict['customerPwd']=orders.customerPwd
                tomorrowDict['sourceName']=orders.sourceName
                tomorrowDict['customerName']=orders.customerName
                tomorrowDict['explain']=orders.explain
                tomorrowDict['notComple']=orders.notComple
                tomorrowList.append(tomorrowDict)
    if request.GET.get('search','')=='':
        month = int(time.strftime('%m', time.localtime(time.time())))
        year = int(time.strftime('%Y', time.localtime(time.time())))
        day = int(time.strftime('%d', time.localtime(time.time())))
        monthList = list(range(1, 13))
        yearList = list(range(2019, 2030))
        return render(request, 'alltomorrow.html', locals())
    else:
        return HttpResponse(json.dumps(tomorrowList))
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