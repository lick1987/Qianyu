from django.conf.urls import url
from .views import *



app_name='order'

urlpatterns = [
    url(r'^$',order_view,name='order'),
    url(r'^deletOrder/(\d*)$',deletOrder_views,name='deletOrder'),
    url(r'^modifyOrder/(\d*)$',modifyOrder,name='modifyOrder'),
    url(r'^addOrder$',addOrder_views,name='addOrder'),
]
