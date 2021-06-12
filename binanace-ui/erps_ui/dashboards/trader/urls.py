
__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^real_trader', views.real_trader, name='real_trader'),
    url(r'^delete_real_trader', views.delete_real_trader, name='delete_real_trader'),
    url(r'^identity_change_real_trader', views.identity_change_real_trader, name='identity_change_real_trader'),
    url(r'^demo_trader', views.demo_trader, name='demo_trader'),
    url(r'^delete_demo_trader', views.delete_demo_trader, name='delete_demo_trader'),
]
