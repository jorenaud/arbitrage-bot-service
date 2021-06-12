
__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^symbols', views.symbols, name='symbols'),
    url(r'^ticks', views.ticks, name='ticks'),
    url(r'^get_ticks', views.get_ticks, name='get_ticks'),
    url(r'^symbase', views.symbase, name='symbase'),
    url(r'^symgroup', views.symgroup, name='symgroup'),
    url(r'^get_symbols', views.get_symbols, name='get_symbols'),
    url(r'^delete_symbol', views.delete_symbol, name='delete_symbol'),
    url(r'^add_symbol', views.add_symbol, name='add_symbol'),
    url(r'^edit_symbol', views.edit_symbol, name='edit_symbol'),
]
