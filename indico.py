#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 10/03/2021

import hashlib
import hmac
import time
import requests
import pandas as pd
import bs4

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def build_indico_request(path, params, api_key=None, secret_key=None, only_public=True, persistent=False):
    """Building an indico request
     Indico allows you to programmatically access the content of its database by exposing various information like category contents, events, rooms and room bookings through a web service, the HTTP Export API.
    The basic URL looks like:
    http://my.indico.server/export/WHAT/[LOC/]ID.TYPE?PARAMS&ak=KEY&timestamp=TS&signature=SIG
    where:

    WHAT    is the element you want to export (one of categ, event, room, reservation)
    LOC     is the location of the element(s) specified by ID and only used for certain elements, for example, for the room booking (https://indico.server/export/room/CERN/120.json?ak=0…)
    ID      is the ID of the element you want to export (can be a - separated list). As for example, the 120 in the above URL.
    TYPE    is the output format (one of json, jsonp, xml, html, ics, atom, bin)
    PARAMS  are various parameters affecting (filtering, sorting, …) the result list
    KEY, TS, SIG are part of the API Authentication.
    https://docs.getindico.io/en/stable/http_api/access/ """

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


def parse_jsonreq(url):
    """We will parse JSON response into Python Dictionary so you can access JSON
    data using key-value pairs. Also, you can prettyPrint JSON in the readable format.
    The requests module provides a builtin JSON decoder, we can use it when we are dealing
    with JSON data. Just execute response.json(), and that’s it. response.json() returns a JSON
    response in Python dictionary format so we can access JSON using key-value pairs.
    https://pynative.com/parse-json-response-using-python-requests-library/"""
    from requests.exceptions import HTTPError
    try:
        response = requests.get(url)
        response.raise_for_status()
        # access JSON content
        jsonResponse = response.json()
        print("Entire JSON response")
        # print(jsonResponse)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return jsonResponse


def build_event_df(dfjs):
    """Build a pandas event dataframe from the returned JSON dictionary."""

    df = pd.DataFrame(columns=['Date and time', 'title', 'location', 'description', 'url'])

    for i in range(len(dfjs["results"])):
        datentime = dfjs["results"][i]["startDate"]["date"] + ' ' + dfjs["results"][i]["startDate"]["time"][:5]
        addr = dfjs["results"][i]["location"]
        title = dfjs["results"][i]["title"]
        url = dfjs["results"][i]["url"]

        d1 = dfjs["results"][i]["description"]
        description = bs4.BeautifulSoup(d1, "html.parser").text

        # description = dfjs["results"][i]["description"]#.getText()
        df.loc[i] = [datentime, addr, title, description, url]
    return df


def indico_requests(categories=[662, 127, 776, 740, 294, 193, 641, 810, 807, 647]):
    """Loop through a list of categories to retrieve events from today plus 60 days in the future
    on the DESY indico website.
    This function takes as input a list of ints corresponding to the DESY indico category numbers.
    For example, https://indico.desy.de/category/807/ would be the CDCS seminar category of
    number 807. If no inputs are given, the default categories are searched through.
    Finally, the events are combined into one event dataframe. """
    df = pd.DataFrame(columns=['Date and time', 'title', 'location', 'description', 'url'])
    PARAMS = {
        'limit': 123,
        'from': 'today',
        'to': '60d10h',
        'pretty': 'yes'
    }

    for cat in categories:
        PATH = 'https://indico.desy.de/export/categ/' + str(cat) + '.json'
        dfjs = parse_jsonreq(build_indico_request(PATH, PARAMS))
        dfnew = build_event_df(dfjs)
        df = pd.concat([df, dfnew]).reset_index(drop=True)
    return df


if __name__ == '__main__':
    # API_KEY = '00000000-0000-0000-0000-000000000000'
    # SECRET_KEY = '00000000-0000-0000-0000-000000000000'
    dfs = indico_requests()
    # print(dfs)