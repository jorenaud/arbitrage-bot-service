
__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^real_trading', views.real_trading, name='real_trading'),
    url(r'^get_real_trading', views.get_real_trading, name='get_real_trading'),
    url(r'^demo_trading', views.demo_trading, name='demo_trading'),
    url(r'^get_demo_trading', views.get_demo_trading, name='get_demo_trading'),
]
