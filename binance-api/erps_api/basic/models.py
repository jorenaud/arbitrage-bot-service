from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class menu_tree(models.Model):
    parent_id = models.IntegerField(default=0)
    has_child = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    level = models.IntegerField(default=0)


class privilege(models.Model):
    name = models.CharField(max_length=255)


class access_history(models.Model):
    username = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)
    ip_addr = models.CharField(max_length=255)
    serverName = models.CharField(max_length=200, default='')
    tradeType = models.CharField(max_length=200, default='')


class event_history(models.Model):
    username = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    part = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)
    ip_addr = models.CharField(max_length=255)

class cmenu_tree(models.Model):
    parent_id = models.IntegerField(default=0)
    has_child = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    level = models.IntegerField(default=0)


class role(models.Model):
    name = models.CharField(max_length=200, default='')


class plan(models.Model):
    name = models.CharField(max_length=200, default='')
    duration = models.IntegerField(default=7)
    description = models.CharField(max_length=200, default='')


class user(models.Model):
    firstName = models.CharField(max_length=100, default='')
    lastName = models.CharField(max_length=100, default='')
    userName = models.CharField(max_length=200, default='')
    email = models.EmailField(default=None)
    phone = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=400, default='')
    country = models.CharField(max_length=100, default='')
    language = models.CharField(max_length=100, default='')
    status = models.IntegerField(default=0) # 1: logout, 2: login, -1: close, 0: no email, 3: trading
    balance = models.CharField(max_length=1000000, default='')
    apiKey = models.CharField(max_length=500, default='')
    apiSecret = models.CharField(max_length=500, default='')
    role = models.IntegerField(default=0)
    planId = models.IntegerField(default=0)
    regTime = models.DateTimeField(default=timezone.now)
    expireTime = models.DateTimeField(default=timezone.now)
    verify = models.BooleanField(default=True)


class adminemails(models.Model):
    emailType = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')


class orders(models.Model):
    userName = models.IntegerField(default=0)
    orderId = models.IntegerField(default=0)
    currency = models.CharField(max_length=200, default='')
    time = models.DateTimeField(default=timezone.now)
    size = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    commission = models.FloatField(default=0.0)
    side = models.CharField(max_length=200, default='')
    orderType = models.CharField(max_length=200, default='')
    botId = models.IntegerField(default=0)
    barTime = models.DateTimeField(default=timezone.now)


class interval(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')


class botList(models.Model):
    userName = models.CharField(max_length=200, default='')
    botID = models.IntegerField(default=0)
    quantity = models.FloatField(default=0.0)
    status = models.BooleanField(default=False)


class price(models.Model):
    name = models.CharField(max_length=200, default='')


class bot(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    currency = models.CharField(max_length=200, default='')
    intervalId = models.IntegerField(default=0)
    priceId = models.IntegerField(default=0)
    period = models.IntegerField(default=0)
    source = models.IntegerField(default=1)


class news(models.Model):
    name = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=20000, default='')
    date = models.DateTimeField(default=timezone.now)
    flag = models.BooleanField(default=False)
    barTime = models.DateTimeField(default=timezone.now)
    botId = models.IntegerField(default=0)
