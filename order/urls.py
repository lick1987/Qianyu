from django.conf.urls import url
from .views import *



app_name='order'

urlpatterns = [
    url(r'^$',order_view,name='order'),
    url(r'^deletOrder/(\d*)$',deletOrder_views,name='deletOrder'),
    url(r'^modifyOrder/(\d*)$',modifyOrder,name='modifyOrder'),
    url(r'^getStatus$',get_status,name='getStatus'),
    url(r'^status/(.+)/$',status_views,name='status'),
    url(r'^changeShow$',change_show,name='changeShow'),
    url(r'^getCustomer$',get_Customer,name='getCustomer'),
    url(r'^getUnit$',get_Unit,name='getUnit'),
    url(r'^deletSource/(\d*)$', deletOrder_views, name='deletSource'),
    url(r'^orderDate/(\d*)$', orderDate_views, name='orderDate'),
    url(r'^changeOrderDate$', changeOrderDate_views, name='changeOrderDate'),
    url(r'^againOrder/(\d*)$', againOrder_views, name='againOrder'),
    url(r'^upload/(\d*)$', upload_views, name='upload'),
    url(r'^deltUpload/(\d*)$', deltUpload_views, name='deltUpload'),
    url(r'^saveOrder/$', saveOrder_views, name='saveOrder'),
]
