from django.conf.urls import url
from .views import *



app_name='customer'

urlpatterns = [
    url(r'^$',customer_view,name='customer'),
    url(r'^deletCuster/(\d*)$',deletCuster_views,name='deletCuster'),
    url(r'^modifyCuster/(\d*)$',modifyCuster,name='modifyCuster'),
    url(r'^addCuster$',addCuster_views,name='addCuster'),
]
