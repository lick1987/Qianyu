from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$',index_views),
    url(r'^unit$',unit_views),
    url(r'^deletUnit/(\d*)',deleteUnit_views),
    url(r'^modifyUnit/(\d*)',modifyUnit_views),
    url(r'^modifyUnit1',modifyUnit_views1),
    url(r'^checkLogin',check_login_views),
    url(r'^register',register_view),
    url(r'^checkname',check_name_view),
    url(r'^exit',exit_view),
    url(r'^addUnit',addUnit_view),



]