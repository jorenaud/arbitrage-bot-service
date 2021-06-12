import requests
import json

from django.core import serializers
from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponse
from erps_ui.dashboards.common import constant as my_constant
from erps_ui.dashboards.common import common as my_common
from datetime import datetime, timedelta

import uuid
import hashlib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

email_verify_enable = True

def welcome(request):
    menu_data = requests.get(my_constant.cmenu_url)
    menu_data = menu_data.json()
    menu_data = menu_data['results']
    new_menu_data = []
    for menu in menu_data:
        if menu["level"] >= 3:
            new_menu_data.append({"id": menu["id"], "parent_id": menu["parent_id"], "has_child": menu["has_child"],
                                  "name": menu["name"], "icon": menu["icon"], "url": menu["url"]})

    return render(request, 'cusomter_template/welcome/index.html', {
        'menudata': new_menu_data
    })


def signup(request):
    menu_data = requests.get(my_constant.cmenu_url)
    menu_data = menu_data.json()
    menu_data = menu_data['results']
    new_menu_data = []
    for menu in menu_data:
        if menu["level"] >= 3:
            new_menu_data.append({"id": menu["id"], "parent_id": menu["parent_id"], "has_child": menu["has_child"],
                                  "name": menu["name"], "icon": menu["icon"], "url": menu["url"]})

    return render(request, 'cusomter_template/account/signup.html', {
        'menudata': new_menu_data
    })


def adduser(request):
    try:
        params = request.POST
        firstname = params.get("firstName", None)
        lastname = params.get("lastName", None)
        email = params.get("email", None)
        phone = params.get("phone", None)

        userid = hash_userid(firstname, lastname, email, phone)
        password = params.get("password", None)
        #password = hash_password(password)

        newparams = params.dict()
        newparams['userName'] = userid
        newparams['password'] = password
        newparams['role'] = 2
        plan = {}
        plan['name'] = "free"
        plans = my_common.ApiRequests(my_constant.plan_url, "GET", plan)
        if len(plans) != 1:
            return HttpResponse('Plan Settings is failed', status=503)
        newparams['planId'] = plans[0]['id']
        newparams['expireTime'] = (datetime.now() + timedelta(days=plans[0]['duration'])).strftime("%Y-%m-%dT%H:%M:%S")
        res = requests.post(my_constant.users_url, json=newparams)
        if res.status_code >= 300:
            return HttpResponse(str(res._content), status=res.status_code)

        res = email_verify(userid, email, password)
        if res < 0:
            return HttpResponse('Email Verification is failed', status=501)

        return HttpResponse("", status=200)

    except Exception as e:
        print(str(e))
        return HttpResponse("status_code = 500", status=500)


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    #password, salt = hashed_password.split(':')
    #return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
    return hashed_password == user_password


def hash_userid(firstname, lastname, email, phone):
    s = firstname + lastname + email + phone
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8

def email_verify(userid, email, password=""):

    if userid == '' or email == '':
        return -1 # uerid or email is null

    emailtype = 'gmail'
    params = {}
    params['emailType'] = emailtype
    adminemail = requests.get(my_constant.adminemails, json=params)
    if adminemail.status_code >= 300:
        return -3 # admin email error
    adminemail = adminemail.json()
    adminemail = adminemail['results']
    count = len(adminemail)
    if count != 1:
        return -4 # admin email error
    adminemail = adminemail[0]

    if emailtype == 'gmail' and email_verify_enable is True:

        message = MIMEMultipart("alternative")
        message["Subject"] = "Binance Email Verification"

        message["From"] = adminemail["email"]
        message["To"] = email

        html = "<html><body><p style='font-size:20px;'>Welcome to Binancer Trading Platform! <br><br>UserID: " + str(
            userid) + "<br> Password: " + password + "<br><br>Thank you.\n</p></body></html>"

        part = MIMEText(html, "html")
        message.attach(part)

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.ehlo()
        s.starttls()
        s.login(adminemail['email'], adminemail["password"])
        s.sendmail(adminemail["email"], email, message.as_string())
        s.close()
        return 0
    elif emailtype == 'outlook' and email_verify_enable is True:
        return 1
    return 2


def login(request):
    menu_data = requests.get(my_constant.cmenu_url)
    menu_data = menu_data.json()
    menu_data = menu_data['results']
    new_menu_data = []
    for menu in menu_data:
        if menu["level"] >= 3:
            new_menu_data.append({"id": menu["id"], "parent_id": menu["parent_id"], "has_child": menu["has_child"],
                                  "name": menu["name"], "icon": menu["icon"], "url": menu["url"]})

    return render(request, 'cusomter_template/account/login.html', {
        'menudata': new_menu_data,
    })


def auth(request):
    userid = ""
    try:
        params = request.POST
        userid = params.get('userid', None)
        password = params.get('password', None)
        if userid == None:
            HttpResponse('Please Insert user ID', status=404)
        params = {}
        params['userName'] = userid
        trader = requests.get(my_constant.users_url, json=params)

        if trader.status_code >= 300:
            return HttpResponse(str(trader._content), status=trader.status_code)

        trader = trader.json()
        trader = trader['results']
        count = len(trader)
        if count != 1:
            return HttpResponse('The user is not registered.', status=502)
        trader = trader[0]
        res = check_password(trader["password"], password)

        if res == False:
            return HttpResponse('Please Insert Correct password', status=503)
        if trader["status"] == -1:
            return HttpResponse('This Account was closed', status=504)

        request.session["BinanceUserName"] = userid   #  modify by jonathan 5/28/2020 10:53AM
        request.session["BinancePassword"] = password
        request.session["BinanceRole"] = trader['role']
        request.session["BinanceUID"] = trader['id']

        params['status'] = 2
        res = requests.put(my_constant.users_url + str(trader['id']) + "/", json=params)
        if res.status_code >= 300:
            my_common.trace_access_history(request, params["userName"], "Fail", request.get_host())
            return HttpResponse('Log In Failed', status=505)

        my_common.trace_access_history(request, params["userName"], "Login", request.get_host())
        return HttpResponse(str(userid), status=200)

    except Exception as e:
        print(str(e))
        my_common.trace_access_history(request, userid, "Fail", request.get_host())
        return HttpResponse("Exception Error", status=500)


def configuration(request):
    return render(request, 'cusomter_template/welcome/configuration.html')


def pricing(request):
    return render(request, 'cusomter_template/welcome/pricing.html')
