from django.conf.urls import url
from .views import *



app_name='source'

urlpatterns = [
    url(r'^$',source_view,name='source'),
    url(r'^modifyCuster/(\d*)$',modifyCuster_view,name='modifyCuster'),
    url(r'^addSource$',addSource_views,name='addSource'),

]
