from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests
import json

from django.core import serializers
from datetime import datetime
from django.shortcuts import render
# from .models import menu_tree as usps_menu
from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant
from django.shortcuts import redirect


def history(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    response = my_common.ApiRequests(my_constant.depositWithdraw_url, "GET")

    length = len(response)
    for i in range(length):
        info = response[length - 1 - i]
        if info['type'] == 0:
            type = 'deposit'
        else:
            type = 'withdraw'
        body_data.append({'uid': info['id'], 'id': i+1, 'userId': info['userId'], 'userFirstName': info['userFirstName'],
                          'userLastName': info['userLastName'], 'userEmail': info['userEmail'], 'userPhone': info['userPhone'],
                          'userAccountBased': info['userAccountBased'], 'type': type, 'amount': str(info['amount']),
                          'updateDate': info['updateDate'], 'balance': str(info['balance'])})

    response = my_common.ApiRequests(my_constant.trader_url, "GET")

    return render(request, 'erps_template/depositWithdraw/history.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'userList': response,
    })


def get_history(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []

    GetData = request.GET
    trader = GetData.get("trader", None)
    params = {}
    if trader is not None and trader != 'all':
        params['userId'] = trader
    else:
        params['userId'] = 'all'

    type = GetData.get("type", None)
    if type is not None and type != 'all':
        params['type'] = int(type)
    else:
        params['type'] = 2

    response = my_common.ApiRequests(my_constant.depositWithdraw_url, "GET", params)

    length = len(response)
    for i in range(length):
        info = response[length - 1 - i]
        if info['type'] == 0:
            type = 'deposit'
        else:
            type = 'withdraw'
        body_data.append(
            {'uid': info['id'], 'id': i + 1, 'userId': info['userId'], 'userFirstName': info['userFirstName'],
             'userLastName': info['userLastName'], 'userEmail': info['userEmail'], 'userPhone': info['userPhone'],
             'userAccountBased': info['userAccountBased'], 'type': type, 'amount': str(info['amount']),
             'updateDate': info['updateDate'], 'balance': str(info['balance'])})

    return HttpResponse(json.dumps(body_data))

def statistics(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []
    response = my_common.ApiRequests(my_constant.trader_url, "GET")
    depowiths = my_common.ApiRequests(my_constant.depositWithdraw_url, "GET")

    id = 1
    for trader in response:
        temp = GetDepoWithTrader(trader, depowiths)
        if len(temp) <= 0:
            continue
        temp['uid'] = trader['id']
        temp['id'] = id
        body_data.append(temp)
        id = id + 1

    userList = []
    id = 1
    for info in response:
        userList.append({'uid': info['id'], 'id': id, 'userId': info['userId'], 'userEmail': info['userEmail']})
        id = id + 1

    return render(request, 'erps_template/depositWithdraw/statistics.html', {
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'userList': userList,
    })


def get_statistics(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    body_data = []
    params = request.GET
    user = params.get("trader", None)

    depowiths = my_common.ApiRequests(my_constant.depositWithdraw_url, "GET")

    if user == 'all':
        response = my_common.ApiRequests(my_constant.trader_url, "GET")

        id = 1
        for trader in response:
            temp = GetDepoWithTrader(trader, depowiths)
            if len(temp) <= 0:
                continue
            temp['uid'] = trader['id']
            temp['id'] = id
            body_data.append(temp)
            id = id + 1
    elif user == 'total':
        temp = GetDepoWithTrader(user, depowiths)
        if len(temp) > 0:
            temp['uid'] = 1
            temp['id'] = 1
            body_data.append(temp)
    else:
        newpa = {}
        newpa['userId'] = user
        trader = my_common.ApiRequests(my_constant.trader_url, "GET", newpa)
        if len(trader) == 1:
            trader = trader[0]
            temp = GetDepoWithTrader(trader, depowiths)
            if len(temp) > 0:
                temp['uid'] = 1
                temp['id'] = 1
                body_data.append(temp)
    return HttpResponse(json.dumps(body_data))

def GetDepoWithTrader(trader, depowiths):

    try:
        if trader == 'total':

            result = {}
            totalBalance = 0
            totaldeposits = 0
            totalwithdraw = 0
            for depowith in depowiths:
                if depowith['type'] == 0:
                    totaldeposits = totaldeposits + depowith['amount'] * depowith['priceRate']
                if depowith['type'] == 1:
                    totalwithdraw = totalwithdraw + depowith['amount'] * depowith['priceRate']

            result['userId'] = 'Total'
            result['userFirstName'] = ''
            result['userLastName'] = ''
            result['userEmail'] = ''
            result['totaldeposit'] = round(totaldeposits, 2)
            result['totalwithdraw'] = round(totalwithdraw, 2)
            result['minute'] = round(totaldeposits - totalwithdraw, 2)

            response = my_common.ApiRequests(my_constant.trader_url, "GET")
            for user in response:
                totalBalance = totalBalance + user['balance']

            result['balance'] = round(totalBalance, 2)
            result['profit'] = round(result['minute'] - totalBalance, 2)

        else:
            result = {}
            totaldeposits = 0
            totalwithdraw = 0
            for depowith in depowiths:
                if trader['userId'] != depowith['userId']:
                    continue
                if depowith['type'] == 0:
                    totaldeposits = totaldeposits + depowith['amount'] * depowith['priceRate']
                if depowith['type'] == 1:
                    totalwithdraw = totalwithdraw + depowith['amount'] * depowith['priceRate']

            result['userId'] = trader['userId']
            result['userFirstName'] = trader['userFirstName']
            result['userLastName'] = trader['userLastName']
            result['userEmail'] = trader['userEmail']
            result['totaldeposit'] = round(totaldeposits, 2)
            result['totalwithdraw'] = round(totalwithdraw, 2)
            result['minute'] = round(totaldeposits - totalwithdraw, 2)
            result['balance'] = round(trader['balance'], 2)
            result['profit'] = round(result['minute'] - trader['balance'], 2)
    except Exception as e:
        print(str(e))
        result = {}
    return result

def add_record(request):
    try:
        params = request.POST.dict()
        if int(params['amount']) <= 0:
            return HttpResponse("Adding Error, Reason: Balance is not validated!", status=501)
        args = {}
        args['userId'] = params['userId']
        user = my_common.ApiRequests(my_constant.trader_url, "GET", args)
        if len(user) != 1:
            return HttpResponse("Adding Error, Reason: " + args['userId'] + " is not existed!", status=502)
        user = user[0]
        if params['type'] == '0':
            params['priceRate'] = GetBasedTimes('USD', params['userAccountBased'])
            balance = user['balance'] + float(params['amount']) * params['priceRate']
        else:
            params['priceRate'] = GetBasedTimes('USD', params['userAccountBased'], 1)
            balance = user['balance'] - float(params['amount']) * params['priceRate']
        if balance < 0:
            return HttpResponse("Adding Error, Reason: " + args['userId'] + " 's Balance is not Enough!", status=503)
        args['balance'] = round(balance, 2)
        params['balance'] = round(balance, 2)
        params['updateDate'] = str(datetime.now())
        result = my_common.ApiRequests(my_constant.trader_url + str(user['id']) + '/', "PUT", args)
        if result.status_code > 300:
            return HttpResponse("Adding Error, Reason: " + args['userId'] + " is not validate to save balance!", status=504)
        result = my_common.ApiRequests(my_constant.depositWithdraw_url, "POST", params)
        if result.status_code > 300:
            return HttpResponse("Adding Error, Reason: " + args['userId'] + " record is not validate to save record!", status=505)
        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse("Adding Error, Reason: exception happened", status=506)

def GetBasedTimes(based, other, flag=0):

    if based == other:
        return 1
    newSymbol = other + based
    params = {}
    params['name'] = newSymbol
    response = my_common.ApiRequests(my_constant.symbols_url, "GET", params)
    if len(response) == 1:
        if flag == 0:
            return response[0]['bid']
        else:
            return response[0]['ask']

    newSymbol = based + other
    params['name'] = newSymbol
    response = my_common.ApiRequests(my_constant.symbols_url, "GET", params)
    if len(response) == 1:
        if flag == 0:
            return 1 / response[0]['ask']
        else:
            return 1 / response[0]['bid']
    return 1
