__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    url(r'^insert_vendor', views.insert_vendor, name='insert_vendor'),
    url(r'^delete_vendor', views.delete_vendor, name='delete_vendor'),
    url(r'^update_vendor', views.update_vendor, name='update_vendor'),
    url(r'^edit_vendor_view', views.edit_vendor_view, name='edit_vendor_view'),
    url(r'^add_vendor_view', views.add_vendor_view, name='add_vendor_view'),
]
