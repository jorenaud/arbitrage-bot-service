from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import json

from django.core import serializers

from django.shortcuts import render
# from .models import menu_tree as usps_menu

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant
from django.shortcuts import redirect


def real_trading(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []


    response = my_common.ApiRequests(my_constant.realtradinghistory_url, "GET")

    id = 1
    length = len(response)
    for i in range(length):
        info = response[length - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'transactionID': info['transactionID'], 'userId': info['userId'],
                          'symbol': info['symbol'], 'timeFrame': info['timeFrame'], 'orderType': info['orderType'],
                          'lotSize': str(info['lotSize']), 'openPrice': str(info['openPrice']),
                          'closePrice': str(info['closePrice']), 'openTime': info['openTime'], 'closeTime': info['closeTime'],
                          'profit': str(info['profit']), 'swap': str(info['swap'])})
        id = id + 1


    response = my_common.ApiRequests(my_constant.trader_url, "GET")
    userList = []
    id = 1
    for info in response:
        userList.append({'uid': info['id'], 'id': id, 'userId': info['userId'], 'userEmail': info['userEmail']})
        id = id + 1

    return render(request, 'erps_template/tradinghistory/real_trading.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'userList': userList,
    })




def demo_trading(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []


    response = my_common.ApiRequests(my_constant.demotradinghistory_url, "GET")

    length = len(response)
    id = 1
    for i in range(length):
        info = response[length - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'transactionID': info['transactionID'], 'userId': info['userId'],
                          'symbol': info['symbol'], 'timeFrame': info['timeFrame'], 'orderType': info['orderType'],
                          'lotSize': str(info['lotSize']), 'openPrice': str(info['openPrice']),
                          'closePrice': str(info['closePrice']), 'openTime': info['openTime'], 'closeTime': info['closeTime'],
                          'profit': str(info['profit']), 'swap': str(info['swap'])})
        id = id + 1


    response = my_common.ApiRequests(my_constant.demotrader_url, "GET")
    userList = []
    id = 1
    for info in response:
        userList.append({'uid': info['id'], 'id': id, 'userId': info['userId'], 'userEmail': info['userEmail']})
        id = id + 1


    return render(request, 'erps_template/tradinghistory/demo_trading.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'userList': userList,
    })




def get_real_trading(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    params = request.GET
    trader = params.get("trader", None)
    params = {}
    if trader is not None and trader != 'all':
        params['userId'] = trader
    else:
        params['userId'] = 'all'

    response = my_common.ApiRequests(my_constant.realtradinghistory_url, "GET", params)

    id = 1
    length = len(response)
    for i in range(length):
        info = response[length - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'transactionID': info['transactionID'], 'userId': info['userId'],
                          'symbol': info['symbol'], 'timeFrame': info['timeFrame'], 'orderType': info['orderType'],
                          'lotSize': str(info['lotSize']), 'openPrice': str(info['openPrice']),
                          'closePrice': str(info['closePrice']), 'openTime': info['openTime'], 'closeTime': info['closeTime'],
                          'profit': str(info['profit']), 'swap': str(info['swap'])})
        id = id + 1

    return HttpResponse(json.dumps(body_data))


def get_demo_trading(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []
    params = request.GET
    trader = params.get("trader", None)
    params = {}
    if trader is not None and trader != 'all':
        params['userId'] = trader
    else:
        params['userId'] = 'all'


    response = my_common.ApiRequests(my_constant.demotradinghistory_url, "GET", params)
    length = len(response)
    id = 1
    for i in range(length):
        info = response[length - 1 - i]
        body_data.append({'uid': info['id'], 'id': id, 'transactionID': info['transactionID'], 'userId': info['userId'],
                          'symbol': info['symbol'], 'timeFrame': info['timeFrame'], 'orderType': info['orderType'],
                          'lotSize': str(info['lotSize']), 'openPrice': str(info['openPrice']),
                          'closePrice': str(info['closePrice']), 'openTime': info['openTime'], 'closeTime': info['closeTime'],
                          'profit': str(info['profit']), 'swap': str(info['swap'])})
        id = id + 1

    return HttpResponse(json.dumps(body_data))


