#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 04/03/2021

import requests, bs4, re
import pandas as pd

def meetup_ds_hamburg(url='https://www.meetup.com/Hamburg-Data-Science-Meetup/events/'):
    """ This is an event scraper for meetup events. Inputs are the event page URL and
    the output contains a dataframe with the next event of this meetup group. """
    urlsep = url.split('/')

    res = requests.get(url)
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    type(noStarchSoup)
    if not noStarchSoup.select(
            '#mupMain > div.groupPageWrapper--child > div.child-wrapper > div > div > div > div.flex-item.flex-item--4 > div > div > ul > li') == None:
        # get the entire event card
        elems = noStarchSoup.select(
            '#mupMain > div.groupPageWrapper--child > div.child-wrapper > div > div > div > div.flex-item.flex-item--4 > div > div > ul > li')
        # print("----------------------------------------------------------------")
        elemst = noStarchSoup.findAll('span', attrs={'class': 'eventTimeDisplay-startDate'})
        elemstitle = noStarchSoup.findAll('span', attrs={'class': 'visibility--a11yHide'})
        description = noStarchSoup.findAll('p', attrs={'class': 'text--small padding--top margin--halfBottom'})
        addr = noStarchSoup.findAll('address')
        datentime = elemst[0].getText()

        # dateRegex = re.compile(r'\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d\d\,')
        # dates = dateRegex.findall(datentime)
        # import datefinder
        # matches = list(datefinder.find_dates(datentime))
        # # time = re.findall(r'\s\d+\:\d\d\s[aAmMpP]+', datentime)
        #
        # d = {'DateTime': [matches[0]]}
        # df1 = pd.DataFrame(data=d)
        # date = df1['DateTime'].dt.strftime('%Y-%m-%d')
        # time = df1['DateTime'].dt.strftime('%H:%M')
        from .helper import split_datetime
        date,time = split_datetime(elemst[0].getText())

        aelem = noStarchSoup.findAll('a', attrs={'class': "eventCard--link" })
        urle = aelem[0]['href'].split('/')
        urles = url+urle[-2]

        dfdict = {'date': date, "time": time,"title": elemstitle[0].getText(), "location": addr[0].getText(),
                  "description": description[1].getText(), 'url': urles}
        df = pd.DataFrame(dfdict, index=[0])
        print(df)
        return df



def combine_dfs():
    return df

if __name__ == "__main__":
    meetup_ds_hamburg()
    # meetup_ds_hamburg(url='https://www.meetup.com/ARIC-Brown-Bag-Sessions/events/')
    # crawl_ahoi(url='https://ahoi.digital/aktuelle/')

# meetup_ds_hamburg('https://www.meetup.com/datamadness-hamburg/events/')

