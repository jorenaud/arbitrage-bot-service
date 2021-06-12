from django.http import HttpResponse
import requests
import hashlib
import datetime

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant


# Create your views here.

def login(request):

    params = request.POST.copy()

    user_info = requests.get(my_constant.users_url)
    user_info = user_info.json()
    user_info = user_info['results']
    params['userlevel'] = -1
    for info in user_info:
        if info["username"] == params["username"] and info["password"] == hashlib.md5(params["password"].encode()).hexdigest():
            params['userid'] = info['id']
            params['userlevel'] = info["is_superuser"]
            params['status'] = info['is_active']
            break

        # if info["email"] == params["username"] and info["password"] == hashlib.md5(
        #         params["password"].encode()).hexdigest():
        #     userlevel = info["is_superuser"]
        #     break

    if params['userlevel'] != -1:
        print(params)
        if params['status'] == 1:
            request.session["username"] = params["username"]
            request.session["userid"] = params["userid"]
            request.session["userlevel"] = params['userlevel']
            my_common.trace_access_history(request, params["username"], "Login", request.get_host())
            return HttpResponse("success")
        else:
            my_common.trace_access_history(request, params["username"], "Fail", request.get_host())
            return HttpResponse("unallowed")            
    else:
        my_common.trace_access_history(request, params["username"], "Fail", request.get_host())
        return HttpResponse("fail")


def logout(request):
    user_name = request.session.get("username", None)

    if user_name is not None:
        request.session["username"] = None
        request.session["userlevel"] = None
        my_common.trace_access_history(request, user_name, "Logout", request.get_host())
        return HttpResponse("success")

    return HttpResponse("fail")


def register_user(request):
    params = request.POST

    new_params = {}

    for key, value in params.items():
        new_params[key] = value

    new_params["password"] = hashlib.md5(new_params["password"].encode()).hexdigest()
    new_params["is_superuser"] = 2
    new_params["is_active"] = 0
    new_params["date_joined"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")

    print(new_params)

    res = requests.post(my_constant.users_url, json=new_params)

    if res.status_code < 300:
        my_common.trace_event_history(request, "---", "Register", "Success", "/Register/" + new_params["username"],
                                      request.get_host())
        return HttpResponse("success")
    else:
        my_common.trace_event_history(request, "---", "Register", "Fail", "/Register/" + new_params["username"],
                                      request.get_host())
        return HttpResponse("fail")


