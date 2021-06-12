from django.shortcuts import render
from django.http import HttpResponse
import requests

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant


# Create your views here.

def delete_user(request):
    params = request.POST

    res = requests.delete(my_constant.users_url + params["id"] + "/")

    user_name = request.session.get("username", None)
    if res.status_code < 300:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Delete", "Success",
                                          "/Setting/User/" + params["username"], request.get_host())
        return HttpResponse("success")
    else:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Delete", "Fail", "/Setting/User/" + params["username"],
                                          request.get_host())
        return HttpResponse("fail")


def update_user(request):
    params = request.POST

    new_params = {}

    new_params["username"] = params["username"]
    new_params["first_name"] = params["firstname"]
    new_params["last_name"] = params["lastname"]
    new_params["email"] = params["email"]
    new_params["mobile"] = params["mobile"]
    new_params["is_superuser"] = params["privilege"]
    new_params["is_active"] = params["status"]

    res = requests.put(my_constant.users_url + str(params["id"]) + "/", json=new_params)

    user_name = request.session.get("username", None)
    if res.status_code < 300:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Update", "Success",
                                          "/Setting/User/" + params["username"], request.get_host())
        return HttpResponse("success")
    else:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Update", "Fail",
                                          "/Setting/User/" + params["username"], request.get_host())
        return HttpResponse("fail")


def edit_user_view(request):
    params = request.POST.copy()

    privilege_info = requests.get(my_constant.privilege_url)
    privilege_info = privilege_info.json()
    privilege_info = privilege_info['results']

    return render(request, 'erps_template/setting/edituser.html', {
        'userdata': params,
        'privilegeinfo': privilege_info
    })


def user_view(request):

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Username"})
    header_data.append({"name": "First Name"})
    header_data.append({"name": "Last Name"})
    header_data.append({"name": "Email"})
    header_data.append({"name": "Mobile"})
    header_data.append({"name": "User Type"})
    header_data.append({"name": "Active"})
    header_data.append({"name": "Joined date"})
    header_data.append({"name": "Action"})

    try:
        user_info = requests.get(my_constant.users_url)
        user_info = user_info.json()
        user_info = user_info['results']

    except Exception as e:
        print(str(e))
        user_info = []

    privilege_info = requests.get(my_constant.privilege_url)
    privilege_info = privilege_info.json()
    privilege_info = privilege_info['results']
    privilege_data = {}
    for privilege in privilege_info:
        privilege_data[str(privilege["id"])] = privilege["name"]

    id = 1
    for info in user_info:
        body_data.append({"uid": info["id"], "id": id, "username": info["username"], "firstname": info["first_name"],
                          "lastname": info["last_name"], "email": info["email"], "mobile": info["mobile"],
                          "privilege": privilege_data[str(info["is_superuser"])], "active": info["is_active"]})
        id = id + 1

    return render(request, 'erps_template/setting/user.html', {'headerdata': header_data, 'bodydata': body_data})



def server_view(request):

    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Server Name"})
    header_data.append({"name": "Server Details"})
    header_data.append({"name": "Server Url"})
    header_data.append({"name": "Server Host"})
    header_data.append({"name": "Server Port"})
    header_data.append({"name": "Status"})
    header_data.append({"name": "Action"})

    try:
        server_info = requests.get(my_constant.servers_rul)
        server_info = server_info.json()
        server_info = server_info['results']

    except Exception as e:
        print(str(e))
        server_info = []

    privilege_info = requests.get(my_constant.privilege_url)
    privilege_info = privilege_info.json()
    privilege_info = privilege_info['results']
    privilege_data = {}
    for privilege in privilege_info:
        privilege_data[str(privilege["id"])] = privilege["name"]


    id = 1
    for info in server_info:
        if info["status"] == 0:
            status = "running"
        else:
            status = "stop"
        body_data.append({"uid": info["id"], "id": id, "serverName": info["serverName"], "serverDetails": info["serverDetails"],
                          "serverUrl": info["serverUrl"], "serverHost": info["serverHost"], "serverPort": info["serverPort"], "status": status})
        id = id + 1

    return render(request, 'erps_template/setting/servers.html', {'headerdata': header_data, 'bodydata': body_data})




