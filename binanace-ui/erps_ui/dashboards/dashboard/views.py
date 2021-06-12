from django.http import HttpResponse
import requests
import json

from django.core import serializers

from django.shortcuts import render
# from .models import menu_tree as usps_menu

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
import time
from datetime import datetime
import tzlocal
from datetime import timedelta

# Create your views here.

def welcome(request):
    return render(request, 'erps_template/dashboard/welcome.html')


def login(request):
    return render(request, 'erps_template/dashboard/login.html')


def register(request):
    return render(request, 'erps_template/dashboard/register.html')


def index(request):
    user_name = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)

    if user_name is None:
        return render(request, "erps_template/dashboard/error.html")

    menu_data = requests.get(my_constant.menu_url)
    menu_data = menu_data.json()
    menu_data = menu_data['results']
    # menudata = usps_menu.objects.all()
    # menu_data = []
    # for menu in menudata:
    #     menu_data.append({"id": menu.id, "parent_id": menu.parent_id, "has_child": menu.has_child, "name": menu.name,
    #                       "icon": menu.icon, "url": menu.url, })

    new_menu_data = []
    for menu in menu_data:
        if menu["level"] >= user_level:
            new_menu_data.append({"id": menu["id"], "parent_id": menu["parent_id"], "has_child": menu["has_child"],
                                  "name": menu["name"], "icon": menu["icon"], "url": menu["url"]})

    return render(request, 'erps_template/dashboard/index.html', {
        'menudata': new_menu_data,
        'username': user_name,
        'userlevel': request.session.get('userlevel', None),
    })


def dashboardView(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    params = {}
    params['active'] = 1
    response = ApiRequests(my_constant.brokeraccount_url, "GET", params)


    if len(response) > 0:
        value = response[0]
        value = round(value['equity'], 2)
    else:
        value = 0

    hourlyData = []
    statistics = ApiRequests(my_constant.statisticsData_url, "GET")
    response = my_common.CalculateHourlyStatics(statistics)
    for info in response:

        dt = datetime(info['year'], info['month'], info['day'], info['hour'])

        milliseconds = int(round(dt.timestamp() * 1000))
        hourlyData.append({'time': milliseconds, 'value': info['profit']})

    dailyData = []
    statistics = ApiRequests(my_constant.statisticsData_url, "GET")
    response = my_common.CalculateDailyStatics(statistics)
    for info in response:
        dt = datetime(info['year'], info['month'], info['day'])

        milliseconds = int(round(dt.timestamp() * 1000))

        dailyData.append({'time': milliseconds, 'value': info['profit']})

    response = ApiRequests(my_constant.trader_url, "GET")
    tradersCount = len(response)
    tradingCount = 0
    webCount = 0
    noEmail = 0
    closeCount = 0
    logoutCount = 0
    timezoneoffset = GetUTCTimeOffset()
    for trader in response:
        if trader['userStatus'] == 3:
            tradingCount += 1
        elif trader['userStatus'] == 2:
            webCount += 1
        elif trader['userStatus'] == 0:
            noEmail += 1
        elif trader['userStatus'] == -1:
            closeCount += 1
        else:
            logoutCount += 1

    return render(request, 'erps_template/dashboard/dashboard.html', {
        'value': value,
        'hourlyData': hourlyData,
        'dailyData': dailyData,
        'tradersCount': tradersCount,
        'tradingCount': tradingCount,
        'webCount': webCount,
        'noEmail': noEmail,
        'closeCount': closeCount,
        'logoutCount': logoutCount,
        'servertimezoneoffset': -timezoneoffset.seconds * 1000,
    })

def GetTradersStatus(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    response = ApiRequests(my_constant.trader_url, "GET")
    tradersCount = len(response)
    tradingCount = 0
    webCount = 0
    noEmail = 0
    closeCount = 0
    logoutCount = 0
    tradersStatus = []
    for trader in response:
        if trader['userStatus'] == 3:
            tradingCount += 1
        elif trader['userStatus'] == 2:
            webCount += 1
        elif trader['userStatus'] == 0:
            noEmail += 1
        elif trader['userStatus'] == -1:
            closeCount += 1
        else:
            logoutCount += 1
    tradersStatus.append(tradersCount)
    tradersStatus.append(tradingCount)
    tradersStatus.append(webCount)
    tradersStatus.append(logoutCount)
    tradersStatus.append(noEmail)
    tradersStatus.append(closeCount)

    return HttpResponse(json.dumps(tradersStatus))


def GetHourlyProfit(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    hourlyData = []
    response = ApiRequests(my_constant.statisticsData_url, "GET")
    response = my_common.CalculateHourlyStatics(response)
    for info in response:
        dt = datetime(info['year'], info['month'], info['day'], info['hour'])

        milliseconds = int(round(dt.timestamp() * 1000))
        hourlyData.append({'time': milliseconds, 'value': info['profit']})

    return HttpResponse(json.dumps(hourlyData))



def GetDailyProfit(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    dailyData = []
    statistics = ApiRequests(my_constant.statisticsData_url, "GET")
    response = my_common.CalculateDailyStatics(statistics)
    for info in response:
        dt = datetime(info['year'], info['month'], info['day'])

        milliseconds = int(round(dt.timestamp() * 1000))
        dailyData.append({'time': milliseconds, 'value': info['profit']})

    return HttpResponse(json.dumps(dailyData))



def GetCurrentMinuteProfit(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    params = {}
    params['active'] = 1
    response = ApiRequests(my_constant.brokeraccount_url, "GET", params)

    if len(response) > 0:
        value = response[0]
        value = round(value['equity'], 2)
    else:
        value = 0
    return HttpResponse(value)



def ApiRequests(url, type, params=None):
    try:
        if type == "GET":
            if params is None:
                response = requests.get(url)
            else:
                response = requests.get(url, json=params)
            response = response.json()
            response = response['results']
        elif type == "POST":
            if params is None:
                response = []
            else:
                response = requests.post(url, json=params)
        elif type == "PUT":
            if params is None:
                response = []
            else:
                response = requests.put(url, json=params)
        elif type == "DELETE":
            response = requests.delete(url)
    except Exception as e:
        print(str(e))
        response = []
    return response


def GetUTCTimeOffset():
    local_tz = tzlocal.get_localzone()
    millis = 1288483950000
    ts = millis * 1e-3
    local_dt = datetime.fromtimestamp(ts, local_tz)
    utc_offset = local_dt.utcoffset()
    return utc_offset
