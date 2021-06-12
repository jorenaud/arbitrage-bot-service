__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^adduser', views.adduser, name='adduser'),
    url(r'^login/', views.login, name='login'),
    url(r'^auth/', views.auth, name='auth'),
    url(r'^pricing/', views.pricing, name='pricing'),
    url(r'^configuration/', views.configuration, name='configuration'),
]
