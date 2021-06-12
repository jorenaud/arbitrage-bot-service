__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    path('', views.welcome, name='welcome'),
    # path('', views.login, name='login'),
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^index', views.index, name='index'),
    url(r'^dashboard', views.dashboardView, name='dashboard'),
    url(r'^GetCurrentMinuteProfit', views.GetCurrentMinuteProfit, name='GetCurrentMinuteProfit'),
    url(r'^GetHourlyProfit', views.GetHourlyProfit, name='GetHourlyProfit'),
    url(r'^GetDailyProfit', views.GetDailyProfit, name='GetDailyProfit'),
    url(r'^GetTradersStatus', views.GetTradersStatus, name='GetTradersStatus'),

]
