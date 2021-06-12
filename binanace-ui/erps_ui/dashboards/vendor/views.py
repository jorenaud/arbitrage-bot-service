from django.http import HttpResponse
import requests
import json

from django.shortcuts import render
# from .models import menu_tree as usps_menu

from erps_ui.dashboards.common import common as my_common
from erps_ui.dashboards.common import constant as my_constant

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


# Create your views here.

def index(request):
    header_data = []
    body_data = []

    header_data.append({"name": "ID"})
    header_data.append({"name": "Company Name"})
    header_data.append({"name": "Domain Address"})
    header_data.append({"name": "Keywords"})
    header_data.append({"name": "Action"})

    try:
        response = requests.get(my_constant.vendor_url)
        response = response.json()
        response = response['results']
    except Exception as e:
        print(str(e))
        response = []

    id = 1
    for info in response:
        body_data.append({"uid": info["id"], "id": id, "name": info["name"], "domain": info["domain"], "keywords": info["keywords"]})

        id = id + 1

    return render(request, 'erps_template/vendor/index.html', {'headerdata': header_data, 'bodydata': body_data})



def delete_vendor(request):
    params = request.POST

    res = requests.delete(my_constant.vendor_url + params["id"] + "/")

    user_name = request.session.get("username", None)
    if res.status_code < 300:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Delete", "Success",
                                          "/vendor/" + params["id"], request.get_host())
        return HttpResponse("success")
    else:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Delete", "Fail", "/vendor/" + params["id"],
                                          request.get_host())
        return HttpResponse("fail")


def update_vendor(request):
    params = request.POST

    new_params = {}

    new_params["name"] = params["name"]
    new_params["domain"] = params["domain"]
    new_params["keywords"] = params["keywords"]

    res = requests.put(my_constant.vendor_url + str(params["id"]) + "/", json=new_params)

    user_name = request.session.get("username", None)
    if res.status_code < 300:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Update", "Success",
                                          "/vendor/" + params["id"], request.get_host())
        return HttpResponse("success")
    else:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Update", "Fail",
                                          "/vendor/" + params["id"], request.get_host())
        return HttpResponse("fail")

def insert_vendor(request):
    params = request.POST

    new_params = {}

    new_params["name"] = params["name"]
    new_params["domain"] = params["domain"]
    new_params["keywords"] = params["keywords"]

    res = requests.post(my_constant.vendor_url, json=new_params)

    user_name = request.session.get("username", None)
    if res.status_code < 300:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Insert", "Success",
                                          "/vendor", request.get_host())
        return HttpResponse("success")
    else:
        if user_name is not None:
            my_common.trace_event_history(request, user_name, "Insert", "Fail",
                                          "/vendor", request.get_host())
        return HttpResponse("fail")


def edit_vendor_view(request):
    params = request.POST
    return render(request, 'erps_template/vendor/editvendor.html', {'userdata': params})

def add_vendor_view(request):
    return render(request, 'erps_template/vendor/addvendor.html')
