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
from erps_ui.dashboards.common.ENUM import *

def real_trader(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "FirstName"})
    header_data.append({"name": "LastName"})
    header_data.append({"name": "Email"})
    #header_data.append({"name": "Phone"})
    header_data.append({"name": "UserID"})
    header_data.append({"name": "Identity Proof"})
    header_data.append({"name": "Country"})
    header_data.append({"name": "Account Based"})
    header_data.append({"name": "Balance"})
    header_data.append({"name": "Equity"})
    header_data.append({"name": "Margin"})
    header_data.append({"name": "Free Margin"})
    header_data.append({"name": "Margin Level"})
    header_data.append({"name": "Total Profit"})
    header_data.append({"name": "Status"})
    header_data.append({"name": "Action"})

    try:
        response = requests.get(my_constant.trader_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for info in response:
        body_data.append({'uid': info['id'], 'id': id, 'firstname': info['userFirstName'], 'lastname': info['userLastName'],
                          'email': info['userEmail'], 'userId': info['userId'], 'identityProof': int(info['userIdentityProof']),
                          'country': info['userCountry'], 'accountBased': info['userAccountBased'], 'balance': round(info['balance'], 2),
                          'equity': round(info['equity'], 2), 'margin': round(info['margin'], 2), 'freeMargin': round(info['freeMargin'], 2),
                          'marginLevel': round(info['marginLevel'], 2), 'totalProfit': round(info['totalProfit'], 2),
                          'status': trader_status(info['userStatus']).name})
        id = id + 1

    return render(request, 'erps_template/trader/real_trader.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })


def delete_real_trader(request):
    try:
        params = request.POST
        userId = params.get('userId')
        id = params.get('uid')

        if userId is None or userId == '' or id is None or id == '':
            return HttpResponse('Undefined the user ID', status=303)
        result = my_common.ApiRequests(my_constant.trader_url + str(id) + "/", "DELETE")
        if result.status_code > 300:
            return HttpResponse('Deleting Error, Reason: API Request Failed!', status=303)

        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Deleting Error, Reason: Exception Happened!', status=304)


def identity_change_real_trader(request):
    try:
        params = request.POST
        id = params.get('uid')
        identity = params.get("identity")

        if identity is None or id is None or id == '':
            return HttpResponse('Undefined the user ID', status=303)
        params = {}
        params['userIdentityProof'] = identity
        result = my_common.ApiRequests(my_constant.trader_url + str(id) + "/", "PUT", params)
        if result.status_code > 300:
            return HttpResponse('Deleting Error, Reason: API Request Failed!', status=303)

        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Deleting Error, Reason: Exception Happened!', status=304)

def demo_trader(request):
    user_id = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)
    if user_level is None or user_id is None:
        return redirect("/broker")

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "FirstName"})
    header_data.append({"name": "LastName"})
    header_data.append({"name": "Email"})
    #header_data.append({"name": "Phone"})
    header_data.append({"name": "UserID"})
    header_data.append({"name": "Account Based"})
    header_data.append({"name": "Balance"})
    header_data.append({"name": "Equity"})
    header_data.append({"name": "Margin"})
    header_data.append({"name": "Free Margin"})
    header_data.append({"name": "Margin Level"})
    header_data.append({"name": "Total Profit"})
    header_data.append({"name": "Status"})
    header_data.append({"name": "Action"})

    try:
        response = requests.get(my_constant.demotrader_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for info in response:
        body_data.append({'uid': info['id'], 'id': id, 'firstname': info['userFirstName'], 'lastname': info['userLastName'], 'email': info['userEmail'],
                          'userId': info['userId'], 'accountBased': info['userAccountBased'], 'balance': round(info['balance'], 2),
                          'equity': round(info['equity'], 2), 'margin': round(info['margin'], 2), 'freeMargin': round(info['freeMargin'], 2),
                          'marginLevel': round(info['marginLevel'], 2), 'totalProfit': round(info['totalProfit'], 2), 'status': trader_status(info['userStatus']).name})
        id = id + 1

    return render(request, 'erps_template/trader/demo_trader.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })



def delete_demo_trader(request):
    try:
        params = request.POST
        userId = params.get('userId')
        id = params.get('uid')

        if userId is None or userId == '' or id is None or id == '':
            return HttpResponse('Undefined the user ID', status=303)
        result = my_common.ApiRequests(my_constant.demotrader_url + str(id) + "/", "DELETE")
        if result.status_code > 300:
            return HttpResponse('Deleting Error, Reason: API Request Failed!', status=303)

        return HttpResponse('Success', status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse('Deleting Error, Reason: Exception Happened!', status=304)
