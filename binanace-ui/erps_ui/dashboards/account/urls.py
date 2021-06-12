
__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^overview', views.overview, name='overview'),
    url(r'^statistics', views.statistics, name='statistics'),
    url(r'^get_overview', views.get_overview, name='get_overview'),
    url(r'^get_statistics', views.get_statistics, name='get_statistics'),
]
