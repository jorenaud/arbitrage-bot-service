import os


api_proto = "http"
# api_host = "192.168.2.111"
api_host = "localhost"
api_port = "8001"

if os.getenv('ERP_API_PROTO') != None: api_proto = os.getenv('ERP_API_PROTO')
if os.getenv('ERP_API_HOST') != None: api_host = os.getenv('ERP_API_HOST')
if os.getenv('ERP_API_PORT') != None: api_port = os.getenv('ERP_API_PORT')

api_url = api_proto + "://" + api_host + ":" + api_port + "/"

menu_url = api_url + "menu/"
privilege_url = api_url + "privilege/"
users_url = api_url + "user/"
roles_url = api_url + "roles/"
botList_url = api_url + "botList/"
bot_url = api_url + "bot/"
interval_url = api_url + "interval/"
price_url = api_url + "price/"
plan_url = api_url + "plans/"
news_url = api_url + "news/"

accesshistory_url = api_url + "accesshistory/"
eventhistory_url = api_url + "eventhistory/"

request_header = {'Content-type' : 'application/json'}

HttpResponse_OK = 200
HttpResponse_Created = 201
HttpResponse_Accepted = 202
HttpResponse_NonAuthoritativeInformation = 203
HttpResponse_NoContent = 204

HttpResponse_BadRequest = 400
HttpResponse_Unauthorized = 401
HttpResponse_PaymentRequired = 402
HttpResponse_Forbidden = 403
HttpResponse_NotFound = 404
HttpResponse_MethodNotAllowed = 405
HttpResponse_NotAcceptable = 406
HttpResponse_ProxyAuthenticationRequired = 407
HttpResponse_RequestTimeout = 408
HttpResponse_Conflict = 409
HttpResponse_Gone = 410

HttpResponse_InternalServerError = 500

cmenu_url = api_url + "cmenu/"
trader_url = api_url + "trader/"
demotrader_url = api_url + "demotrader/"
adminemails = api_url + "adminemails/"


orders_url = api_url + "orders/"
demotrading_url = api_url + "demotrading/"
symbols_url = api_url + "symbols/"
ticks_url = api_url + "ticks/"


realtradinghistory_url = api_url + "realtradinghistory/"
demotradinghistory_url = api_url + "demotradinghistory/"

brokeraccount_url = api_url + "brokeraccount/"

statisticsData_url = api_url + "statisticsData/"

depositWithdraw_url = api_url + "depositWithdraw/"

servers_rul = api_url + "servers/"

symbase_url = api_url + "symBase/"

symgroup_url = api_url + "symGroup/"

bars_url = api_url + "bars/"
