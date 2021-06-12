__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    url(r'^delete_user', views.delete_user, name='delete_user'),
    url(r'^update_user', views.update_user, name='update_user'),
    url(r'^edit_user_view', views.edit_user_view, name='edit_user_view'),
    url(r'^user_view', views.user_view, name='user_view'),
    url(r'^server_view', views.server_view, name='servers'),

]
