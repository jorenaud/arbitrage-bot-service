
__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^history', views.history, name='history'),
    url(r'^statistics', views.statistics, name='statistics'),
    url(r'^get_history', views.get_history, name='get_history'),
    url(r'^get_statistics', views.get_statistics, name='get_statistics'),
    url(r'^add_record', views.add_record, name='add_record'),
]
