__author__ = 'com'
# from rest_framework import serializers
from .models import *
from rbasis.serializers import *

class menuTreeSerializer(ShAPISerializer):
    class Meta:
        model = menu_tree
        fields = ('id', 'parent_id', 'has_child', 'name', 'icon', 'url', 'level')


class cmenuTreeSerializer(ShAPISerializer):
    class Meta:
        model = cmenu_tree
        fields = ('id', 'parent_id', 'has_child', 'name', 'icon', 'url', 'level')



class privilegeSerializer(ShAPISerializer):
    class Meta:
        model = privilege
        fields = ('id', 'name')

class accesshistorySerializer(ShAPISerializer):
    class Meta:
        model = access_history
        fields = ('id', 'username', 'type', 'time', 'ip_addr', 'serverName', 'tradeType')


class eventhistorySerializer(ShAPISerializer):
    class Meta:
        model = event_history
        fields = ('id', 'username', 'type', 'result', 'part', 'time', 'ip_addr')


class roleSerializer(ShAPISerializer):
    class Meta:
        model = role
        fields = ('id', 'name')


class planSerializer(ShAPISerializer):
    class Meta:
        model = plan
        fields = ('id', 'name', 'duration', 'description')


class userSerializer(ShAPISerializer):
    class Meta:
        model = user
        fields = ('id', 'firstName', 'lastName', 'userName', 'email',
                  'phone', 'password', 'country', 'language', 'status', 'balance',
                  'apiKey', 'apiSecret', 'role', 'planId', 'regTime', 'expireTime', 'verify')


class adminemailsSerializer(ShAPISerializer):
    class Meta:
        model = adminemails
        fields = ('id', 'emailType', 'email', 'password')


class ordersSerializer(ShAPISerializer):
    class Meta:
        model = orders
        fields = ('id', 'userName', 'orderId', 'currency', 'time', 'size', 'price', 'commission', 'side',
                  'orderType', 'botId', 'barTime')


class intervalSerializer(ShAPISerializer):
    class Meta:
        model = interval
        fields = ('id', 'name', 'description')


class botListSerializer(ShAPISerializer):
    class Meta:
        model = botList
        fields = ('id', 'userName', 'botID', 'quantity', 'status')


class priceSerializer(ShAPISerializer):
    class Meta:
        model = price
        fields = ('id', 'name')


class botSerialzier(ShAPISerializer):
    class Meta:
        model = bot
        fields = ('id', 'name', 'description', 'currency', 'intervalId', 'priceId', 'period', 'source')


class newsSerializier(ShAPISerializer):
    class Meta:
        model = news
        fields = ('id', 'name', 'description', 'date', 'flag', 'barTime', 'botId')
