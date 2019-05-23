import time

from django.shortcuts import render

# Create your views here.
from order.models import *


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
                    sNumber=oDate[0].saveNumber.split(',')
                    str1=''
                    for i in sNumber[5*day:5*day+5]:
                        if i:
                            str1+=i+','
                    if str1:
                        tomorrowDict['arrange']=str1[:-1]
                        tomorrowDict['customerUnit']=orders.customerUnit
                        tomorrowDict['customerPwd']=orders.customerPwd
                        tomorrowDict['sourceName']=orders.sourceName
                        tomorrowList.append(tomorrowDict)


    # total = orderDate.objects.filter(user=id, order=i)
    return render(request,'tomorrow.html',locals())