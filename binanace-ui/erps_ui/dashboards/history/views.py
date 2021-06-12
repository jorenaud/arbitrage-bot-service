from django.shortcuts import render
import requests

from erps_ui.dashboards.common import constant as my_constant


# Create your views here.

def access_view(request):
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

    user_name = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)

    try:
        if user_level == 1:
            access_info = requests.get(my_constant.accesshistory_url)
        else:
            access_info = requests.get(my_constant.accesshistory_url + "?username=" + user_name)

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
        'userlevel': request.session.get('userlevel', None)
    })


def event_view(request):
    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Username"})
    header_data.append({"name": "Type"})
    header_data.append({"name": "Result"})
    header_data.append({"name": "Url"})
    header_data.append({"name": "DateTime"})
    header_data.append({"name": "Access IP"})
    header_data.append({"name": "Action"})

    user_name = request.session.get("username", None)
    user_level = request.session.get("userlevel", None)

    try:
        if user_level == 1:
            event_info = requests.get(my_constant.eventhistory_url)
        else:
            event_info = requests.get(my_constant.eventhistory_url + "?username=" + user_name)

        event_info = event_info.json()
        event_info = event_info['results']
    except Exception as e:
        print(str(e))
        event_info = []

    id = 1
    for i in range(0, len(event_info)):
        info = event_info[len(event_info) - i - 1]
        body_data.append({"uid": info["id"], "id": id, "username": info["username"], "type": info["type"],
                          "result": info["result"], "part": info["part"], "time": info["time"],
                          "ipaddr": info["ip_addr"]})

        id = id + 1

    return render(request, 'erps_template/history/event.html', {
        'headerdata': header_data,
        'bodydata': body_data,
        'userlevel': request.session.get('userlevel', None)
    })
