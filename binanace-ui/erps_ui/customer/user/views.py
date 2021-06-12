from django.shortcuts import render

# Create your views here.
import requests
import json

from django.core import serializers

from django.shortcuts import render
from django.http import HttpResponse
from erps_ui.dashboards.common import constant as my_constant
from django.shortcuts import redirect
from erps_ui.dashboards.common import common as my_common
from datetime import datetime, timedelta
import json


def welcome(request):
    userName = request.session.get("BinanceUserName", None)
    role = request.session.get("BinanceRole", None)
    if role is None or userName is None:
        return redirect("/")

    params = {}
    params['userName'] = userName

    trader = requests.get(my_constant.users_url, json=params)
    trader = trader.json()
    trader = trader['results']
    if len(trader) != 1:
        return redirect("/")
    trader = trader[0]
    request.session["BinanceRole"] = trader["role"]
    role = trader["role"]
    menu_data = requests.get(my_constant.menu_url)
    menu_data = menu_data.json()
    menu_data = menu_data['results']
    new_menu_data = []
    for menu in menu_data:
        if menu["level"] >= role:
            new_menu_data.append({"id": menu["id"], "parent_id": menu["parent_id"], "has_child": menu["has_child"],
                                  "name": menu["name"], "icon": menu["icon"], "url": menu["url"]})

    return render(request, 'erps_template/dashboard/index.html', {
        'menudata': new_menu_data,
        'username': userName,
        'userlevel': role,
    })


def logout(request):
    traderid = request.session.get("BinanceUserName", None)
    ident = request.session.get("BinanceUID", None)
    if traderid is not None:
        request.session["BinanceUserName"] = None
        request.session["BinanceRole"] = None
        request.session["BinanceUID"] = None
        request.session["BinancePassword"] = None
        my_common.trace_access_history(request, traderid, "Logout", request.get_host())
    if ident is None:
        return HttpResponse('Log out Failed', status=505)
    params = {}
    params['status'] = 1

    res = requests.put(my_constant.users_url + str(ident) + "/", json=params)
    if res.status_code >= 300:
        return HttpResponse('Log out Failed', status=res.status_code)
    return HttpResponse(str(traderid), status=200)


def dashboardView(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        response = my_common.ApiRequests(my_constant.users_url, "GET")
        tradersCount = len(response)
        webCount = 0
        noEmail = 0
        logoutCount = 0
        timezoneoffset = my_common.GetUTCTimeOffset()
        params = {}
        params['userName'] = user_id
        orders = my_common.ApiRequests(my_constant.orders_url, "GET", params)
        daily = CalculateDailyProfit(orders)
        for trader in response:
            if trader['status'] == 2:
                webCount += 1
            elif trader['status'] == 0:
                noEmail += 1
            else:
                logoutCount += 1

        return render(request, 'erps_template/dashboard/dashboard.html', {
            'tradersCount': tradersCount,
            'webCount': webCount,
            'noEmail': noEmail,
            'logoutCount': logoutCount,
            'servertimezoneoffset': -timezoneoffset.seconds * 1000,
            'dailyData': daily
        })
    except Exception as e:
        return HttpResponse(str(e), status=500)


def accountView(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    params = {}
    params['userName'] = user_id
    response = my_common.ApiRequests(my_constant.users_url, "GET", params)
    result = []
    if len(response) == 1:
        balances = response[0]['balance']
        balance = {}
        try:
            if balances is not "":
                balance = json.loads(balances)
        except Exception as e:
            print(str(e))
        index = 0
        for key, value in balance.items():
            if index % 2 is 0:
                result.append({'id1': index, 'asset1': key, 'free1': value[0], 'locked1': value[1]})
            else:
                no = int(index / 2)
                result[no]['id2'] = index
                result[no]['asset2'] = key
                result[no]['free2'] = value[0]
                result[no]['locked2'] = value[1]
            index += 1

    return render(request, 'erps_template/account/overview.html', {
        'bodydata': result,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
    })


def accountData(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    params = {}
    params['userName'] = user_id
    response = my_common.ApiRequests(my_constant.users_url, "GET", params)
    result = []
    if len(response) == 1:
        balances = response[0]['balance']
        balance = {}
        try:
            if balances is not "":
                balance = json.loads(balances)
        except Exception as e:
            print(str(e))
        index = 0
        for key, value in balance.items():
            if index % 2 is 0:
                result.append({'id1': index, 'asset1': key, 'free1': value[0], 'locked1': value[1]})
            else:
                no = int(index / 2)
                result[no]['id2'] = index
                result[no]['asset2'] = key
                result[no]['free2'] = value[0]
                result[no]['locked2'] = value[1]
            index += 1

    return HttpResponse(json.dumps(result), status=200)


def tradingView(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")
    params = {}
    params['userName'] = user_id

    if user_level == 1:
        response = my_common.ApiRequests(my_constant.orders_url, "GET")
        users = my_common.ApiRequests(my_constant.users_url, "GET")
    else:
        response = my_common.ApiRequests(my_constant.orders_url, "GET", params)
        users = my_common.ApiRequests(my_constant.users_url, "GET", params)
    result = []
    index = 0

    for i in range(len(response) - 1, -1, -1):
        item = response[i]
        result.append({'id': index, 'userName': item['userName'], 'order': item['orderId'],
                       'currency': item['currency'], 'time': item['time'], 'size': item['size'],
                       'price': item['price'], 'commission': item['commission'],
                       'side': item['side'], 'orderType': item['orderType']})
        index += 1

    return render(request, 'erps_template/trading/real_trading.html', {
        'trading_data': result,
        'userlevel': user_level,
        'hostip': my_constant.api_host,
        'userList': users,
    })


def tradingData(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    params = request.GET
    trader = params.get("trader", None)
    params = {}
    if trader is not None and trader != 'all':
        params['userName'] = trader
    elif trader is None:
        params['userName'] = user_id
    else:
        params['userName'] = 'all'

    response = my_common.ApiRequests(my_constant.orders_url, "GET", params)
    result = []
    index = 0
    for i in range(len(response) - 1, -1, -1):
        item = response[i]
        result.append({'id': index, 'userName': item['userName'], 'order': item['orderId'],
                       'currency': item['currency'], 'time': item['time'], 'size': item['size'],
                       'price': item['price'], 'commission': item['commission'],
                       'side': item['side'], 'orderType': item['orderType']})
        index += 1

    return HttpResponse(json.dumps(result), status=200)


def setting_accountView(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    params = {}
    params['userName'] = user_id
    user = my_common.ApiRequests(my_constant.users_url, "GET", params)
    if user_level == 1:
        users = my_common.ApiRequests(my_constant.users_url, "GET")
    else:
        users = user
    if len(user) != 1:
        return redirect("/")
    roles = my_common.ApiRequests(my_constant.roles_url, "GET")
    plans = my_common.ApiRequests(my_constant.plan_url, "GET")
    user = user[0]
    header_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "F.Name"})
    header_data.append({"name": "L.Name"})
    header_data.append({"name": "UserId"})
    header_data.append({"name": "Email"})
    header_data.append({"name": "Phone"})
    header_data.append({"name": "Cntry"})
    header_data.append({"name": "Lan"})
    header_data.append({"name": "Role"})
    header_data.append({"name": "Plan"})
    header_data.append({"name": "Reg Date"})
    header_data.append({"name": "Expire Date"})
    header_data.append({"name": "Status"})
    header_data.append({"name": "Verify"})
    header_data.append({"name": "Action"})

    return render(request, 'erps_template/datafeeds/account.html', {
        'headerdata': header_data,
        'userlevel': user_level,
        'userList': users,
        'apiKey': user['apiKey'],
        'apiSecret': user['apiSecret'],
        'roles': roles,
        'plans': plans,
        'hostip': my_constant.api_host,
    })


def change_account_plan(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        newParams = {}
        params = request.POST.dict()
        newParams['planId'] = int(params['planId'])
        newParams['expireTime'] = params['expireTime']
        orgPlanId = params['orgPlanId']
        plans = my_common.ApiRequests(my_constant.plan_url, "GET")
        month = None
        for plan in plans:
            if plan['name'] == "monthly":
                month = plan
                break
        if month is None:
            return HttpResponse("monthly plan is not existed", status=507)

        if month['id'] == newParams['planId']:
            expireTime = datetime.strptime(params['expireTime'], "%Y-%m-%dT%H:%M:%SZ")
            if expireTime <= datetime.now():
                expireTime = datetime.now() + timedelta(days=month['duration'])
            newParams['expireTime'] = expireTime.strftime("%Y-%m-%dT%H:%M:%S")

        res = my_common.ApiRequests(my_constant.users_url + str(params['id']) + '/', "PUT", newParams)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def delete_account(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = request.POST.dict()
        if user_id == params['userName']:
            return HttpResponse("You can't delete yourself.", status=508)

        res = my_common.ApiRequests(my_constant.users_url + str(params['id']) + '/', "DELETE")
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def change_account_verify(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = request.POST.dict()
        if params['verify'] == "false":
            params['verify'] = True
        else:
            params['verify'] = False

        params['id'] = int(params['id'])
        res = my_common.ApiRequests(my_constant.users_url + str(params['id']) + '/', "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def change_account_role(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = request.POST.dict()
        if user_id == params['userName']:
            return HttpResponse("You can change your role yourself.", status=205)

        res = my_common.ApiRequests(my_constant.users_url + str(params['id']) + '/', "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def save_api_key_secret(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = {}
        params['userName'] = user_id
        users = my_common.ApiRequests(my_constant.users_url, "GET", params)
        if len(users) != 1:
            return redirect("/")
        ident = users[0]['id']
        params = request.POST.dict()
        res = my_common.ApiRequests(my_constant.users_url + str(ident) + '/', "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def get_setting_accounts(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = {}
        params['userName'] = user_id

        if user_level == 1:
            users = my_common.ApiRequests(my_constant.users_url, "GET")
        else:
            users = my_common.ApiRequests(my_constant.users_url, "GET", params)
        result = users
        for i in range(0, len(result), 1):
            if users[i]['status'] == 1:
                result[i]['status'] = 'Logout'
            elif users[i]['status'] == 2:
                result[i]['status'] = 'Login'
            elif users[i]['status'] == 0:
                result[i]['status'] = 'NoEmail'
            elif users[i]['status'] == 3:
                result[i]['status'] = 'Trading'

        return HttpResponse(json.dumps(result), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def delete_admin_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        params['id'] = int(params['id'])
        args = {}
        args['botID'] = params['id']
        bots = my_common.ApiRequests(my_constant.botList_url, "GET", args)
        for bot in bots:
            my_common.ApiRequests(my_constant.botList_url + str(bot['id']) + "/", "DELETE")
        res = my_common.ApiRequests(my_constant.bot_url + str(params['id']) + "/", "DELETE")

        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def edit_admin_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        params['id'] = int(params['id'])
        res = my_common.ApiRequests(my_constant.bot_url + str(params['id']) + "/", "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def add_admin_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        res = my_common.ApiRequests(my_constant.bot_url, "POST", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def get_admin_bots(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        admin_bots = my_common.ApiRequests(my_constant.bot_url, "GET")
        return HttpResponse(json.dumps(admin_bots), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def change_admin_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        params['id'] = int(params['id'])
        res = my_common.ApiRequests(my_constant.bot_url + str(params['id']) + '/', "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=200)
        return HttpResponse("fail", status=503)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def setting_botView(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")
    if user_level != 1:
        return redirect("/")

    intervals = my_common.ApiRequests(my_constant.interval_url, "GET")
    prices = my_common.ApiRequests(my_constant.price_url, "GET")

    header_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Name"})
    header_data.append({"name": "Description"})
    header_data.append({"name": "Currency"})
    header_data.append({"name": "Time Interval"})
    header_data.append({"name": "Price"})
    header_data.append({"name": "Period"})
    header_data.append({"name": "Source"})
    header_data.append({"name": "Action"})

    return render(request, 'erps_template/datafeeds/admin_bot.html', {
        'headerdata': header_data,
        'userlevel': user_level,
        'intervals': intervals,
        'prices': prices,
        'hostip': my_constant.api_host,
    })


def access_view(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")
    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Username"})
    header_data.append({"name": "Type"})
    header_data.append({"name": "DateTime"})
    header_data.append({"name": "Access IP"})
    header_data.append({"name": "Server Name"})
    header_data.append({"name": "Trade Type"})
    header_data.append({"name": "Action"})

    try:
        if user_level == 1:
            access_info = requests.get(my_constant.accesshistory_url)
        else:
            access_info = requests.get(my_constant.accesshistory_url + "?username=" + user_id)

        access_info = access_info.json()
        access_info = access_info['results']
    except Exception as e:
        print(str(e))
        access_info = []

    id = 1
    for i in range(0, len(access_info)):
        info = access_info[len(access_info) - i - 1]
        body_data.append({"uid": info["id"], "id": id, "username": info["username"], "type": info["type"],
                          "time": info["time"], "ipaddr": info["ip_addr"], "serverName": info["serverName"],
                          "tradeType": info["tradeType"]})

        id = id + 1

    return render(request, 'erps_template/history/access.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': user_level
    })


def on_delete_event(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        if user_level != 1:
            return redirect("/")
        params = request.POST.dict()
        res = my_common.ApiRequests(my_constant.eventhistory_url + str(params['id']) + '/', 'DELETE')
        if res.status_code < 300:
            return HttpResponse('success', status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def on_delete_access(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        if user_level != 1:
            return redirect("/")
        params = request.POST.dict()
        res = my_common.ApiRequests(my_constant.accesshistory_url + str(params['id']) + '/', 'DELETE')
        if res.status_code < 300:
            return HttpResponse('success', status=200)
        return HttpResponse(res.text, status=res.status_code)
    except Exception as e:
        return HttpResponse(str(e), status=500)


def get_event_data(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.GET
        trader = params.get("trader", None)
        params = {}
        if trader is not None and trader != 'all':
            params['userName'] = trader
        elif trader is None:
            params['userName'] = user_id
        else:
            params['userName'] = 'all'
        event_info = my_common.ApiRequests(my_constant.eventhistory_url, "GET", params)
        id = 1
        body_data = []
        for i in range(0, len(event_info)):
            info = event_info[len(event_info) - i - 1]
            result = info["result"].replace("\r\n", " ")
            body_data.append({"uid": info["id"], "id": id, "userName": info["username"], "type": info["type"],
                              "result": result, "part": info["part"], "time": info["time"],
                              "ipaddr": info["ip_addr"]})

            id = id + 1

        return HttpResponse(json.dumps(body_data), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def event_view(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Username"})
    header_data.append({"name": "Type"})
    header_data.append({"name": "Result"})
    header_data.append({"name": "DateTime"})
    #header_data.append({"name": "Action"})

    params = {}
    params['userName'] = user_id

    if user_level == 1:
        event_info = my_common.ApiRequests(my_constant.eventhistory_url, "GET")
        users = my_common.ApiRequests(my_constant.users_url, "GET")
    else:
        event_info = my_common.ApiRequests(my_constant.eventhistory_url, "GET", params)
        users = my_common.ApiRequests(my_constant.users_url, "GET", params)

    id = 1
    for i in range(0, len(event_info)):
        info = event_info[len(event_info) - i - 1]
        result = info["result"].replace("\r\n", " ")
        body_data.append({"uid": info["id"], "id": id, "userName": info["username"], "type": info["type"],
                          "result": result, "part": info["part"], "time": info["time"],
                          "ipaddr": info["ip_addr"]})

        id = id + 1

    return render(request, 'erps_template/history/event.html', {
        'headerdata': header_data,
        'event_data': body_data,
        'userList': users,
        'userlevel': user_level
    })


def bots_view(request):
    user_id = request.session.get("BinanceUserName", None)
    user_level = request.session.get("BinanceRole", None)
    if user_level is None or user_id is None:
        return redirect("/")

    params = {}
    params['userName'] = user_id

    if user_level == 1:
        users = my_common.ApiRequests(my_constant.users_url, "GET")
    else:
        users = my_common.ApiRequests(my_constant.users_url, "GET", params)

    bots = my_common.ApiRequests(my_constant.bot_url, "GET")

    header_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "User ID"})
    header_data.append({"name": "Bot ID"})
    header_data.append({"name": "Name"})
    header_data.append({"name": "Description"})
    header_data.append({"name": "Quantity(%)"})
    header_data.append({"name": "Status"})
    header_data.append({"name": "Action"})

    return render(request, 'erps_template/datafeeds/symbols.html', {
        'headerdata': header_data,
        'userlevel': user_level,
        'userList': users,
        'bots': bots,
        'hostip': my_constant.api_host,
    })


def find_bot(bots, ident):
    if bots is None:
        return None
    for bot in bots:
        if bot["id"] == ident:
            return bot
    return None


def get_bots_list(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = request.GET.dict()
        userName = params.get("userName", None)
        if userName is None:
            return HttpResponse("UserId is None", status=501)

        params = {'userName': userName}
        botList = my_common.ApiRequests(my_constant.botList_url, "GET", params)
        bots = my_common.ApiRequests(my_constant.bot_url, "GET")
        result = []
        for bot in botList:
            admin = find_bot(bots, bot['botID'])
            if admin is None:
                continue
            result.append({'id': bot['id'], 'userName': bot['userName'], 'name': admin['name'],
                           'description': admin['description'], 'quantity': bot['quantity'],
                           'botID': bot['botID'], 'status': bot['status']})

        return HttpResponse(json.dumps(result), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def add_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        userId = params.get("userName", None)
        if userId == "all":
            params['userName'] = "any"
        botID = params.get("botID", None)
        quantity = params.get("quantity", 0)
        params['status'] = 0  # 0 is stop, 1 is running
        if userId is None or botID is None or quantity is 0:
            return HttpResponse("User Id, Bot Id, or Quantity Error", status=501)
        res = my_common.ApiRequests(my_constant.botList_url, "POST", params)
        if res.status_code < 300:
            return HttpResponse("success", status=res.status_code)
        if res.status_code == 555:
            return HttpResponse("Adding Bot Error. Bot is already existed!", status=res.status_code)
        return HttpResponse("Adding Bot Error. Please contact admin!", status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def edit_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        ident = params.get("id", None)
        userName = params.get("userName", None)
        if userName == "all":
            params['userName'] = "any"
        botID = params.get("botID", None)
        quantity = params.get("quantity", 0)
        params['status'] = 0  # 0 is stop, 1 is running
        if ident is None or userName is None or botID is None or quantity is 0:
            return HttpResponse("User Id, Bot Id, or Quantity Error", status=501)

        res = my_common.ApiRequests(my_constant.botList_url + str(ident) + "/", "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=res.status_code)
        return HttpResponse("Edit Bot Error. Please contact admin!", status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def start_stop_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = request.POST.dict()
        userName = params.get("userName", None)
        if userName == "any" and user_level > 1:
            return HttpResponse("You cannot control this bot. Please contact admin!", status=503)

        ident = params.get("id", None)
        status = params.get("status", None)
        if ident is None or userName is None or status is None:
            return HttpResponse("User Id, Bot Id Error", status=501)

        if status == "False" or status == "false" or status == "0":
            params['status'] = True
        else:
            params['status'] = False
        res = my_common.ApiRequests(my_constant.botList_url + str(ident) + "/", "PUT", params)
        if res.status_code < 300:
            return HttpResponse("success", status=res.status_code)
        return HttpResponse("Start/Stop Bot Error. Please contact admin!", status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def delete_bot(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        params = request.POST.dict()
        ident = params.get("id", None)
        params['status'] = 0  # 0 is stop, 1 is running
        if ident is None:
            return HttpResponse("User Id, Bot Id, or Quantity Error", status=501)

        res = my_common.ApiRequests(my_constant.botList_url + str(ident) + "/", "DELETE")
        if res.status_code < 300:
            return HttpResponse("success", status=res.status_code)
        return HttpResponse("Delete Bot Error. Please contact admin!", status=res.status_code)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def get_trading_news(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        news = my_common.ApiRequests(my_constant.news_url, "GET")
        result = []
        for item in news:
            if item['name'] == 'Error':
                continue
            result.append(item)
        return HttpResponse(json.dumps(result), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def FindDailyProfit(dailies, time):
    try:
        for daily in dailies:
            if daily['time'] == time:
                return daily
        return None
    except:
        return None


def CalculateDailyProfit(orders):
    result = []
    profit = 0
    preOrderSide = "None"
    preOrderSize = -1.0
    for order in orders:
        orderTime = datetime.strptime(order['time'], "%Y-%m-%dT%H:%M:%SZ")
        time = datetime(orderTime.year, orderTime.month, orderTime.day)
        time = int(round(time.timestamp() * 1000))
        if order['side'] == "BUY":
            if profit == 0 or preOrderSide == "BUY":
                preOrderSize = float(order['size'])
                profit = -float(order['price']) * preOrderSize
                preOrderSide = order['side']
                continue
            else:
                if preOrderSize == -1.0:
                    preOrderSize = float(order['size'])
                profit -= float(order['price']) * preOrderSize
        elif order['side'] == "SELL":
            if profit == 0 or preOrderSide == "SELL":
                preOrderSize = float(order['size'])
                profit = float(order['price']) * preOrderSize
                preOrderSide = order['side']
                continue
            else:
                if preOrderSize == -1.0:
                    preOrderSize = float(order['size'])
                profit += float(order['price']) * preOrderSize

        daily = FindDailyProfit(result, time)
        if daily is None:
            result.append({'time': time, 'value': profit})
        else:
            daily['value'] += profit
        profit = 0
        preOrderSide = -1.0
    return result


def get_trader_status(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")

        response = my_common.ApiRequests(my_constant.users_url, "GET")
        tradersCount = len(response)
        webCount = 0
        noEmail = 0
        logoutCount = 0
        tradersStatus = []
        for trader in response:
            if trader['status'] == 2:
                webCount += 1
            elif trader['status'] == 0:
                noEmail += 1
            else:
                logoutCount += 1
        tradersStatus.append(tradersCount)
        tradersStatus.append(webCount)
        tradersStatus.append(logoutCount)
        tradersStatus.append(noEmail)

        return HttpResponse(json.dumps(tradersStatus))
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)


def get_daily_profit(request):
    try:
        user_id = request.session.get("BinanceUserName", None)
        user_level = request.session.get("BinanceRole", None)
        if user_level is None or user_id is None:
            return redirect("/")
        params = {}
        params['userName'] = user_id
        orders = my_common.ApiRequests(my_constant.orders_url, "GET", params)
        daily = CalculateDailyProfit(orders)
        return HttpResponse(json.dumps(daily), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e), status=500)

