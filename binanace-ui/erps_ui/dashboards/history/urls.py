__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^access_view', views.access_view, name='access_view'),
    url(r'^event_view', views.event_view, name='event_view'),
]
