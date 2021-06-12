import requests
import json
from datetime import datetime as dt
import tzlocal

from erps_ui.dashboards.common import constant as my_constant


def trace_access_history(request, username, type, ip_addr):
    params = {}

    params["username"] = username
    params["type"] = type
    params["time"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.000000")
    params["ip_addr"] = ip_addr

    return requests.post(my_constant.accesshistory_url, json=params)


def trace_event_history(request, username, type, result, part, ip_addr):
    params = {}

    params["username"] = username
    params["type"] = type
    params["result"] = result
    params["part"] = part
    params["time"] = dt.now().strftime("%Y-%m-%d %H:%M:%S.000000")
    params["ip_addr"] = ip_addr

    return requests.post(my_constant.eventhistory_url, json=params)


def send_request(type, url, data=None, pk=None):
    if type == "get":
        res = requests.get(url)
        if res.status_code != my_constant.HttpResponse_OK:
            res = []
        else:
            res = res.json()
        return res

    if type == "post":
        res = requests.post(url, data=json.dumps(data), headers=my_constant.request_header)
        return res

    if type == "put":
        res = requests.put(url + str(pk) + "/", data=json.dumps(data), headers=my_constant.request_header)
        return res

    if type == "delete":
        res = requests.delete(url + str(pk) + "/")
        return res


def make_absolute_location(base_url, location):
    """
    Convert a location header into an absolute URL.
    """
    absolute_pattern = re.compile(r'^[a-zA-Z]+://.*$')
    if absolute_pattern.match(location):
        return location

    parsed_url = urlparse(base_url)

    if location.startswith('//'):
        # scheme relative
        return parsed_url.scheme + ':' + location

    elif location.startswith('/'):
        # host relative
        return parsed_url.scheme + '://' + parsed_url.netloc + location

    else:
        # path relative
        return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path.rsplit('/', 1)[0] + '/' + location

    return location


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in environ.items():
        # Sometimes, things don't like when you send the requesting host through.
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        elif key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            headers[key.replace('_', '-')] = value

    return headers


def CalculateMinutelyStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            if preRow['year'] == row['year'] and preRow['month'] == row['month'] and preRow['day'] == row['day'] and preRow['hour'] == row['hour'] and preRow['minute'] == row['minute']:
                preRow['profit'] = preRow['profit'] + row['profit']
                continue
            result.append(preRow)
            preRow = row
        if preRow['year'] != 0:
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result


def CalculateHourlyStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['minute'] = 0
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            if preRow['year'] == row['year'] and preRow['month'] == row['month'] and preRow['day'] == row['day'] and preRow['hour'] == row['hour']:
                preRow['profit'] = preRow['profit'] + row['profit']
                continue
            result.append(preRow)
            preRow = row
        if preRow['year'] != 0:
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result

def CalculateDailyStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['hour'] = 0
            row['minute'] = 0
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            if preRow['year'] == row['year'] and preRow['month'] == row['month'] and preRow['day'] == row['day']:
                preRow['profit'] = preRow['profit'] + row['profit']
                continue
            result.append(preRow)
            preRow = row
        if preRow['year'] != 0:
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result


def CalculateMonthlyStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['day'] = 0
            row['hour'] = 0
            row['minute'] = 0
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            if preRow['year'] == row['year'] and preRow['month'] == row['month']:
                preRow['profit'] = preRow['profit'] + row['profit']
                continue
            result.append(preRow)
            preRow = row
        if preRow['year'] != 0:
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result


def CalculateYearlyStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['month'] = 0
            row['day'] = 0
            row['hour'] = 0
            row['minute'] = 0
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            if preRow['year'] == row['year']:
                preRow['profit'] = preRow['profit'] + row['profit']
                continue
            result.append(preRow)
            preRow = row
        if preRow['year'] != 0:
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result


def CalculateTotalStatics(statics):

    try:
        result = []

        preRow = {'year': 0, }
        for row in statics:
            row['month'] = 0
            row['day'] = 0
            row['hour'] = 0
            row['minute'] = 0
            row['second'] = 0
            if preRow['year'] == 0:
                preRow = row
                continue
            preRow['profit'] = preRow['profit'] + row['profit']

        if preRow['year'] != 0:
            preRow['year'] = str(preRow['year']) + " - " + str(row['year'])
            result.append(preRow)
    except Exception as e:
        print(str(e))
        result = []
    return result



def ApiRequests(url, type, params=None):
    response=""
    try:
        if type == "GET":
            if params is None:
                response = requests.get(url)
            else:
                response = requests.get(url, json=params)
            response = response.json()
            response = response['results']
        elif type == "POST":
            if params is None:
                response = []
            else:
                response = requests.post(url, json=params)
        elif type == "PUT":
            if params is None:
                response = []
            else:
                response = requests.put(url, json=params)
        elif type == "DELETE":
            response = requests.delete(url)
    except Exception as e:
        print(str(e))
        response = []
    return response


def GetUTCTimeOffset():
    local_tz = tzlocal.get_localzone()
    millis = 1288483950000
    ts = millis * 1e-3
    local_dt = dt.fromtimestamp(ts, local_tz)
    utc_offset = local_dt.utcoffset()
    return utc_offset
