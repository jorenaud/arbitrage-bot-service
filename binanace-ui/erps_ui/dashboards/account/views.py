from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import json

from django.core import serializers

from django.shortcuts import render
# from .models import menu_tree as usps_menu
from erps_ui.dashboards.common import  common as my_comman
from erps_ui.dashboards.common import constant as my_constant
from django.shortcuts import redirect


def overview(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    response = ApiRequests(my_constant.brokeraccount_url, "GET")
    id = 1
    for info in response:
        if info['active'] == 0:
            active = 'demo'
        else:
            active = 'real'
        countPoPercent = round(info['countPositivePercentage'])
        countNePercet = round(info['countNegativePercentage'])
        nePercent = round(info['negativePercentage'])
        poPercent = round(info['positivePercentage'])
        body_data.append({'uid': info['id'], 'id': id, 'name': info['name'], 'email': info['email'],
                          'balance': str(info['balance']), 'equity': str(info['equity']), 'lastProfit': str(info['lastProfit']),
                          'lastUpdateDate': info['lastUpdateDate'], 'bestProfit': str(info['bestProfit']),
                          'lowestProfit': str(info['lowestProfit']), 'positiveCount': str(info['positiveCount']),
                          'positiveProfit': str(info['positiveProfit']), 'negativeCount': str(info['negativeCount']),
                          'negativeProfit': str(info['negativeProfit']), 'countNegativePercentage': str(countNePercet),
                          'countPositivePercentage': str(countPoPercent), 'negativePercentage': str(nePercent),
                          'positivePercentage': str(poPercent), 'active': active})
        id = id + 1

    return render(request, 'erps_template/account/overview.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })


def get_overview(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    response = ApiRequests(my_constant.brokeraccount_url, "GET")

    id = 1
    for info in response:
        if info['active'] == 0:
            active = 'demo'
        else:
            active = 'real'
        countPoPercent = round(info['countPositivePercentage'])
        countNePercet = round(info['countNegativePercentage'])
        nePercent = round(info['negativePercentage'])
        poPercent = round(info['positivePercentage'])
        body_data.append({'uid': info['id'], 'id': id, 'name': info['name'], 'email': info['email'],
                          'balance': str(info['balance']), 'equity': str(info['equity']), 'lastProfit': str(info['lastProfit']),
                          'lastUpdateDate': info['lastUpdateDate'], 'bestProfit': str(info['bestProfit']),
                          'lowestProfit': str(info['lowestProfit']), 'positiveCount': str(info['positiveCount']),
                          'positiveProfit': str(info['positiveProfit']), 'negativeCount': str(info['negativeCount']),
                          'negativeProfit': str(info['negativeProfit']), 'countNegativePercentage': str(countNePercet),
                          'countPositivePercentage': str(countPoPercent), 'negativePercentage': str(nePercent),
                          'positivePercentage': str(poPercent), 'active': active})
        id = id + 1

    return HttpResponse(json.dumps(body_data))



def statistics(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    response = ApiRequests(my_constant.statisticsData_url, "GET")

    id = 1

    for i in range(0, len(response)):
        info = response[len(response) - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'year': info['year'], 'month': info['month'],
                          'day': info['day'], 'hour': info['hour'], 'minute': info['minute'],
                          'second': info['second'], 'profit': str(info['profit'])})
        id = id + 1

    return render(request, 'erps_template/account/statistics.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })



def get_statistics(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []
    params = request.GET
    statisticstype = params.get("statisticstype", None)

    response = ApiRequests(my_constant.statisticsData_url, "GET")
    if statisticstype == '1':
        response = my_comman.CalculateMinutelyStatics(response)
    elif statisticstype == '2':
        response = my_comman.CalculateHourlyStatics(response)
    elif statisticstype == '3':
        response = my_comman.CalculateDailyStatics(response)
    elif statisticstype == '4':
        response = my_comman.CalculateMonthlyStatics(response)
    elif statisticstype == '5':
        response = my_comman.CalculateYearlyStatics(response)
    elif statisticstype == '6':
        response = my_comman.CalculateTotalStatics(response)

    id = 1
    for i in range(0, len(response)):
        info = response[len(response) - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'year': info['year'], 'month': info['month'],
                          'day': info['day'], 'hour': info['hour'], 'minute': info['minute'],
                          'second': info['second'], 'profit': str(info['profit'])})
        id = id + 1

    return HttpResponse(json.dumps(body_data))




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