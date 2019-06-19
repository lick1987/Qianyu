from django.contrib import admin

from tomorrow.models import tomorrow
from .models import *
from source.models import *
from order.models import *
from customer.models import *


class UnitAdmin(admin.ModelAdmin):
    list_display = ('uname', 'upwd')  # 指定要显示的字段
    search_fields = ('uname',)  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
class userCusterDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer')  # 指定要显示的字段
    search_fields = ('customer',)  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('uphone', 'uwei','uqq','uname')  # 指定要显示的字段
    search_fields = ('uwei',)  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
class tomorrowAdmin(admin.ModelAdmin):
    list_display = ('times', 'customerUnit','sourceName','sourceName')  # 指定要显示的字段
    search_fields = ('sourceName',)  # 指定要搜索的字段，将会出现一个搜索框让管理员搜索关键词
admin.site.register(unit,UnitAdmin)
admin.site.register(customer,CustomerAdmin)
admin.site.register(user)
admin.site.register(allData)
admin.site.register(order)
admin.site.register(orderDate)
admin.site.register(source)
admin.site.register(userSourceData)
admin.site.register(userCusterData,userCusterDataAdmin)
admin.site.register(tomorrow,tomorrowAdmin)