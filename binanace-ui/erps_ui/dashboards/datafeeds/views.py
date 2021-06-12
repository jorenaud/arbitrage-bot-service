from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import json
from datetime import datetime
from django.core import serializers

from django.shortcuts import render
# from .models import menu_tree as usps_menu

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant
from django.shortcuts import redirect
from erps_ui.dashboards.common.ENUM import *

def symbols(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    header_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Symbol"})
    header_data.append({"name": "Description"})
    header_data.append({"name": "Digit"})
    header_data.append({"name": "Base Currency"})
    header_data.append({"name": "Profit Currency"})
    header_data.append({"name": "Margin Currency"})
    header_data.append({"name": "Orders"})
    header_data.append({"name": "Group"})
    header_data.append({"name": "Swap Type"})
    header_data.append({"name": "Swap Long"})
    header_data.append({"name": "Swap Short"})
    header_data.append({"name": "3 Days Swap"})
    header_data.append({"name": "Action"})

    groups = my_common.ApiRequests(my_constant.symgroup_url, "GET")
    return render(request, 'erps_template/datafeeds/symbols.html', {
        'headerdata': header_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'groups': groups,
    })



def ticks(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    try:
        response = requests.get(my_constant.ticks_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for i in range(0, len(response)):
        if i > 100:
            break
        info = response[len(response) - i - 1]
        body_data.append({'uid': info['id'], 'id': id, 'symbol': info['symbol'], 'date': info['date'],
                          'bid': str(info['bid']), 'ask': str(info['ask']), 'last': str(info['last']),
                          'volume': str(info['volume'])})
        id = id + 1

    try:
        response = requests.get(my_constant.symbols_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []


    symbolList = []
    id = 1
    for info in response:
        symbolList.append({'uid': info['id'], 'id': id, 'name': info['name']})
        id = id + 1

    return render(request, 'erps_template/datafeeds/ticks.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'symbols': symbolList
    })


def get_ticks(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    params = request.POST
    symbol = params.get("symbol", None)

    params = {}
    if symbol is not None and symbol != 'all':
        params['symbol'] = symbol
    else:
        params['symbol'] = 'all'
    body_data = []

    try:
        response = requests.get(my_constant.ticks_url, json=params)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for i in range(0, len(response)):
        if i > 100:
            break
        info = response[len(response) - i - 1]
        body_data.append({'uid': info['id'], 'id': id, 'symbol': info['symbol'], 'date': info['date'],
                          'bid': str(info['bid']), 'ask': str(info['ask']), 'last': str(info['last']),
                          'volume': str(info['volume'])})
        id = id + 1

    return HttpResponse(json.dumps(body_data))

def symbase(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Server Name"})
    header_data.append({"name": "Base Info"})
    header_data.append({"name": "Company Name"})
    header_data.append({"name": "Lang Url"})
    header_data.append({"name": "Currency"})
    header_data.append({"name": "Digits"})
    header_data.append({"name": "Receive UserMsg"})
    header_data.append({"name": "Account Method"})
    header_data.append({"name": "Margin Mode"})
    header_data.append({"name": "Action"})

    try:
        response = requests.get(my_constant.symbase_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for info in response:
        body_data.append({'uid': info['id'], 'id': id, 'serverName': info['serverName'], 'baseInfo': info['baseInfo'],
                          'companyName': info['companyName'], 'langUrl': info['langUrl'], 'currency': info['currency'],
                          'digits': str(info['digits']), 'receiveUserMsg': str(info['receiveUserMsg']),
                          'accMethod': PosAccMethod(info['accMethod']).name,
                          'marginMode': MarginMode(info['marginMode']).name})
        id = id + 1

    return render(request, 'erps_template/datafeeds/symbase.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })



def symgroup(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Group Name"})
    header_data.append({"name": "Trade Mode"})
    header_data.append({"name": "Trade Type"})
    header_data.append({"name": "Fill Policy"})
    header_data.append({"name": "Expiration"})
    header_data.append({"name": "Order Flag"})
    header_data.append({"name": "Initial Margin"})
    header_data.append({"name": "Maint Margin"})
    header_data.append({"name": "Swap Type"})
    header_data.append({"name": "Swap Long"})
    header_data.append({"name": "Swap Short"})
    header_data.append({"name": "3Days Swap"})
    header_data.append({"name": "Action"})

    try:
        response = requests.get(my_constant.symgroup_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for info in response:
        body_data.append({'uid': info['id'], 'id': id, 'groupName': info['groupName'],
                          'tradeMode': TradeMode(info['tradeMode']).name,
                          'tradeType': TradeType(info['tradeType']).name,
                          'fillPolicy': FillPolicy(info['fillPolicy']).name,
                          'expiration': ExpirationDate(info['expiration']).name, 'orderFlag': info['orderFlag'],
                          'initialMargin': str(info['initialMargin']),
                          'maintenanceMargin': str(info['maintenanceMargin']),
                          'swapType': SwapType(info['swapType']).name,
                          'swapLong': str(info['swapLong']), 'swapShort': str(info['swapShort']),
                          'threeDaysSwap': V3DaysSwap(info['threeDaysSwap']).name})
        id = id + 1

    return render(request, 'erps_template/datafeeds/symgroup.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })

def get_symbols(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")
    try:
        groupId = request.GET.get("group", None)
    except Exception as e:
        print(str(e))
        groupId = 0

    param = {}
    param['groupId_'] = int(groupId)
    response = my_common.ApiRequests(my_constant.symbols_url, "GET", param)

    return HttpResponse(json.dumps(response))

def delete_symbol(request):
    try:
        params = request.POST
        symbolName = params.get('symbolName')
        id = params.get('uid')

        if symbolName is None or symbolName == '' or id is None or id == '':
            return HttpResponse('Undefined the user ID', status=303)

        result = my_common.ApiRequests(my_constant.symbols_url + str(id) + "/", "DELETE")
        if result.status_code > 300:
            return HttpResponse('Deleting Error, Reason: API Request Failed!', status=503)

        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Deleting Error, Reason: Exception Happened!', status=504)

def add_symbol(request):
    try:
        params = request.POST
        arg = {}
        arg['name'] = params['name']
        symbol = my_common.ApiRequests(my_constant.symbols_url, "GET", arg)
        if len(symbol) != 0:
            return HttpResponse("Adding Error, Reason: " + arg['name'] + " is already existed!", status=502)
        result = my_common.ApiRequests(my_constant.symbols_url, "POST", params)
        if result.status_code > 300:
            return HttpResponse('Adding Error, Reason: API Request Failed!', status=503)
        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Adding Error, Reason: Exception Happened!', status=504)

def edit_symbol(request):
    try:
        params = request.POST
        params = params.dict()
        arg = {}
        arg['name'] = params['name']
        symbol = my_common.ApiRequests(my_constant.symbols_url, "GET", arg)
        if len(symbol) != 1:
            return HttpResponse("Editing Error, Reason: " + arg['name'] + " is not existed!", status=502)
        elif symbol[0]['id'] != int(params['id']):

            return HttpResponse("Editing Error, Reason: " + arg['name'] + " has invalid ID!", status=505)
        params['updateTime'] = str(datetime.now())
        result = my_common.ApiRequests(my_constant.symbols_url + str(symbol[0]['id']) + '/', "PUT", params)
        if result.status_code > 300:
            return HttpResponse('Editing Error, Reason: API Request Failed!', status=503)
        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Editing Error, Reason: Exception Happened!', status=504)
