#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 10/03/2021

import hashlib
import hmac
import time
import requests
import urllib.request
import json
import pandas as pd

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode



def build_indico_request(path, params, api_key=None, secret_key=None, only_public=True, persistent=False):
    items = list(params.items()) if hasattr(params, 'items') else list(params)
    if api_key:
        items.append(('apikey', api_key))
    if only_public:
        items.append(('onlypublic', 'yes'))
    if secret_key:
        if not persistent:
            items.append(('timestamp', str(int(time.time()))))
        items = sorted(items, key=lambda x: x[0].lower())
        url = '%s?%s' % (path, urlencode(items))
        signature = hmac.new(secret_key.encode('utf-8'), url.encode('utf-8'),
                             hashlib.sha1).hexdigest()
        items.append(('signature', signature))
    if not items:
        return path
    return '%s?%s' % (path, urlencode(items))


def parse_json(url):
    res = urllib.request.urlopen(url)
    # res = requests.get(url)
    # res.raise_for_status()
    jdata = []
    for line in json.loads(res.read()):
        jline = json.loads(line.read())
        jdata.append(jline)
    # y = json.loads(res.read())
    # print(y)
    return jdata

def parse_jsonreq(url):
    from requests.exceptions import HTTPError
    try:
        response = requests.get(url)
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        print("Entire JSON response")
        # print(jsonResponse)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return jsonResponse #.items()

def build_event_df(dfjs):

    df = pd.DataFrame(columns=['Date and time', 'title', 'location', 'description', 'url'])

    for i in range(len(dfjs["results"])):
        # print(dfjs["results"][i])
        datentime = dfjs["results"][i]["startDate"]
        addr = dfjs["results"][i]["location"]
        title = dfjs["results"][i]["title"]
        url = dfjs["results"][i]["url"]
        description = dfjs["results"][i]["description"]
        df.loc[i] = [datentime, addr, title, description, url]
    return df


if __name__ == '__main__':
    # API_KEY = '00000000-0000-0000-0000-000000000000'
    # SECRET_KEY = '00000000-0000-0000-0000-000000000000'
    # PATH = '/export/categ/1337.json'  127
    PATH = 'https://indico.desy.de/export/categ/662.json'#?from=today&to=30d10h&pretty=yes'
    PARAMS = {
        'limit': 123,
        'from': 'today',
        'to': '60d10h',
        'pretty': 'yes'
    }

    dfjs = parse_jsonreq(build_indico_request(PATH, PARAMS))
    df = build_event_df(dfjs)
    print(df)
