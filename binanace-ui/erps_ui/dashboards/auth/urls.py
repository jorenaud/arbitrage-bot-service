__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register_user', views.register_user, name='register_user'),
]
