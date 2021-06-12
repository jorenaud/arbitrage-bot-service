__author__ = 'com'

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('account/', views.accountView, name='account'),
    path('get_account_data/', views.accountData, name='account'),
    path('trading/', views.tradingView, name='trading'),
    path('get_trading_data/', views.tradingData, name='trading'),
    path('setting_account/', views.setting_accountView, name='setting_account'),
    path('get_setting_accounts/', views.get_setting_accounts, name='get_setting_accounts'),
    path('save_api_key_secret/', views.save_api_key_secret, name='save_api_key_secret'),
    path('change_account_role/', views.change_account_role, name='change_account_role'),
    path('change_account_verify/', views.change_account_verify, name='change_account_verify'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('change_account_plan/', views.change_account_plan, name='change_account_plan'),
    path('setting_bot/', views.setting_botView, name='setting_bot'),
    path('change_admin_bot/', views.change_admin_bot, name='change_admin_bot'),
    path('get_admin_bots/', views.get_admin_bots, name='get_admin_bots'),
    path('add_admin_bot/', views.add_admin_bot, name='add_admin_bot'),
    path('edit_admin_bot/', views.edit_admin_bot, name='edit_admin_bot'),
    path('delete_admin_bot/', views.delete_admin_bot, name='delete_admin_bot'),
    path('access_view/', views.access_view, name='access_view'),
    path('event_view/', views.event_view, name='event_view'),
    path('get_event_data/', views.get_event_data, name='get_event_data'),
    path('on_delete_event/', views.on_delete_event, name='on_delete_event'),
    path('on_delete_access/', views.on_delete_access, name='on_delete_access'),
    path('bots/', views.bots_view, name='bots_view'),
    path('get_bots_list/', views.get_bots_list, name='get_bots_list'),
    path('add_bot/', views.add_bot, name='add_bot'),
    path('start_stop_bot/', views.start_stop_bot, name='start_stop_bot'),
    path('edit_bot/', views.edit_bot, name='edit_bot'),
    path('delete_bot/', views.delete_bot, name='delete_bot'),
    path('get_trading_news/', views.get_trading_news, name='get_trading_news'),
    path('get_daily_profit/', views.get_daily_profit, name='get_daily_profit'),
    path('get_trader_status/', views.get_trader_status, name='get_trader_status'),
]
