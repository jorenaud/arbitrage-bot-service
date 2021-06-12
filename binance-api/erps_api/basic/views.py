import json
from django.http import HttpResponse
from rest_framework.response import Response
from rbasis.views import *
from .models import *
from .serializers import *

from django.conf import settings

import uuid
import os
import subprocess


# Create your views here.
class menu(ShAPIView):
    queryset = menu_tree.objects.get_queryset().order_by('id')
    serializer_class = menuTreeSerializer
    pass

class cmenu(ShAPIView):
    queryset = cmenu_tree.objects.get_queryset().order_by('id')
    serializer_class = cmenuTreeSerializer
    pass


class privilegeView(ShAPIView):
    queryset = privilege.objects.get_queryset().order_by('id')
    serializer_class = privilegeSerializer
    pass


class userView(ShAPIView):
    queryset = user.objects.get_queryset().order_by('id')
    serializer_class = userSerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        if "username" in request.query_params:
            self.queryset = user.objects.filter(userName=params["username"])

        if ("email" in request.query_params) and ("password" in request.query_params):
            self.queryset = user.objects.filter(email=params["email"], password=params["password"])

        return super().list(request, args, kwargs)

    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            return super().update(request, args, **kwargs)
        except Exception as e:
            print(e)
            return self.log(e)

    def create(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            res = user.objects.filter(email=email)
            if len(res) != 0:
                return HttpResponse("Email is already existed!", status=403)
            return super().create(request, args, kwargs)
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e), status=404)

    def get_queryset(self):
        try:
            userName = self.request.data['userName']
            if userName is None:
                queryset = user.objects.get_queryset().order_by('id')
            else:
                queryset = user.objects.filter(userName=userName)
            return queryset
        except:
            queryset = user.objects.get_queryset().order_by('id')
            return queryset


class accesshistoryView(ShAPIView):
    queryset = access_history.objects.get_queryset().order_by('id')
    serializer_class = accesshistorySerializer

    def list(self, request, *args, **kwargs):
        if len(request.query_params) == 0:
            return super().list(request, args, kwargs)

        params = request.query_params

        if "username" in request.query_params:
            self.queryset = access_history.objects.filter(username=params["username"])

        return super().list(request, args, kwargs)


class eventhistoryView(ShAPIView):
    queryset = event_history.objects.get_queryset().order_by('id')
    serializer_class = eventhistorySerializer

    def get_queryset(self):
        try:
            userName = self.request.data['userName']
            if userName is None or userName == "all":
                queryset = event_history.objects.get_queryset().order_by('id')
            else:
                queryset = event_history.objects.filter(username=userName)
            return queryset
        except:
            queryset = event_history.objects.get_queryset().order_by('id')
            return queryset


class roleView(ShAPIView):
    queryset = role.objects.get_queryset().order_by('id')
    serializer_class = roleSerializer


class planView(ShAPIView):
    queryset = plan.objects.get_queryset().order_by('id')
    serializer_class = planSerializer

    def get_queryset(self):
        try:
            id = self.request.data['id']
            if id is None:
                queryset = plan.objects.get_queryset().order_by('id')
            else:
                queryset = plan.objects.filter(id=id)
            return queryset
        except:
            try:
                name = self.request.data['name']
                if name is None or name == "":
                    queryset = plan.objects.get_queryset().order_by('id')
                else:
                    queryset = plan.objects.filter(name=name)
                return queryset
            except:
                queryset = plan.objects.get_queryset().order_by('id')
                return queryset


class ordersView(ShAPIView):
    queryset = orders.objects.get_queryset().order_by('id')
    serializer_class = ordersSerializer

    def get_queryset(self):
        try:
            userName = self.request.data['userName']
            if userName is None or userName == "all":
                queryset = orders.objects.get_queryset().order_by('id')
            else:
                queryset = orders.objects.filter(userName=userName)
            return queryset
        except:
            queryset = orders.objects.get_queryset().order_by('id')
            return queryset


class adminemailsView(ShAPIView):
    queryset = adminemails.objects.get_queryset().order_by('id')
    serializer_class = adminemailsSerializer

    def get_queryset(self):
        try:
            type = self.request.data['emailType']
            if type is None:
                queryset = adminemails.objects.get_queryset().order_by('id')
            else:
                queryset = adminemails.objects.filter(emailType=type)
            return queryset
        except:
            queryset = adminemails.objects.get_queryset().order_by('id')
            return queryset


class intervalView(ShAPIView):
    queryset = interval.objects.get_queryset().order_by('id')
    serializer_class = intervalSerializer


class botListView(ShAPIView):
    queryset = botList.objects.get_queryset().order_by('id')
    serializer_class = botListSerializer

    def get_queryset(self):
        try:
            userName = self.request.data['userName']
            if userName is None or userName == "all":
                queryset = botList.objects.get_queryset().order_by('id')
            else:
                queryset = botList.objects.filter(userName=userName)
            return queryset
        except:
            try:
                botID = self.request.data['botID']
                queryset = botList.objects.filter(botID=botID)
            except:
                queryset = botList.objects.get_queryset().order_by('id')
            return queryset

    def create(self, request, *args, **kwargs):
        try:
            userName = request.data['userName']
            botID = request.data['botID']
            res = botList.objects.filter(userName=userName, botID=botID)
            if len(res) != 0:
                return HttpResponse("Bot is already existed!", status=555)
            return super().create(request, args, kwargs)
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e), status=404)


class priceView(ShAPIView):
    queryset = price.objects.get_queryset().order_by('id')
    serializer_class = priceSerializer


class botView(ShAPIView):
    queryset = bot.objects.get_queryset().order_by('id')
    serializer_class = botSerialzier

    def create(self, request, *args, **kwargs):
        try:
            currency = request.data['currency']
            intervalId = request.data['intervalId']
            priceId = request.data['priceId']
            period = request.data['period']
            res = bot.objects.filter(currency=currency, intervalId=intervalId,
                                     priceId=priceId, period=period)
            if len(res) != 0:
                return HttpResponse("Bot is already existed!", status=555)
            return super().create(request, args, kwargs)
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e), status=404)


class newsView(ShAPIView):
    queryset = news.objects.get_queryset().order_by('id')
    serializer_class = newsSerializier

    def get_queryset(self):
        try:
            flag = self.request.data['gFlag']
            if flag is None:
                queryset = news.objects.get_queryset().order_by('id')
            else:
                queryset = news.objects.filter(flag=flag)
            return queryset
        except:
            queryset = news.objects.get_queryset().order_by('id')
            return queryset
