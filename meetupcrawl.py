#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 04/03/2021

import requests, bs4, re
import pandas as pd

def meetup_ds_hamburg(url='https://www.meetup.com/Hamburg-Data-Science-Meetup/events/'):
    """ This is an event scraper for meetup events. Inputs are the event page URL and
    the output contains a dataframe with the next event of this meetup group. """

    res = requests.get(url)
    res.raise_for_status()
    noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')
    type(noStarchSoup)
    # elems = noStarchSoup.select('#eventCard-276438418 > div > div:nth-child(1) > div > div > div:nth-child(1)')
    if not noStarchSoup.select('#mupMain > div.groupPageWrapper--child > div.child-wrapper > div > div > div > div.flex-item.flex-item--4 > div > div > ul > li') == None:
        # get the entire event card
        elems = noStarchSoup.select('#mupMain > div.groupPageWrapper--child > div.child-wrapper > div > div > div > div.flex-item.flex-item--4 > div > div > ul > li')
        # print("----------------------------------------------------------------")
        elemst = noStarchSoup.findAll('span', attrs = {'class': 'eventTimeDisplay-startDate'})
        # elemst = noStarchSoup.findAll('span', {'class': ['eventTimeDisplay-startDate','eventCardHead--title']})
        elemstitle = noStarchSoup.findAll('span', attrs = {'class' : 'visibility--a11yHide'})
        description = noStarchSoup.findAll('p', attrs={'class': 'text--small padding--top margin--halfBottom'})
        addr = noStarchSoup.findAll('address')
        datentime = elemst[0].getText()

        # dateRegex = re.compile(r'\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d\d\,')
        # dates = dateRegex.findall(events)
        # times = re.findall(r'\s\d+\:\d\d\s[aAmMpP]+', events)

        dfdict = {'Date and time': datentime, "title": elemstitle[0].getText(), "Location": addr[0].getText(), "description": description[1].getText()}
        df = pd.DataFrame(dfdict, index=[0])
        print(df)
        return df

meetup_ds_hamburg()
# meetup_ds_hamburg('https://www.meetup.com/datamadness-hamburg/events/')

