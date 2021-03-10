#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 10/03/2021

import requests, bs4, re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains


def crawl_ahoi(url='https://ahoi.digital/aktuelle/'):
    """ This is an event scraper for ahoi digital events. Inputs are the event page URL and
    the output contains a dataframe with the next event of this group. """

    # Create our driver object with the headless parameter so that the browser window doesn't open.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Get the page and extract the clock WebElement
    driver.get(url)
    element = driver.find_element_by_id('elementor-tab-title-1642')

    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Now from Selenium to Beautiful Soup
    noStarchSoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    if not noStarchSoup.select('elementor-tab-content-1642') == None:
        # get the entire event
        # elems = noStarchSoup.select('elementor-tab-content-1642')
        # print("----------------------------------------------------------------")
        elemst = noStarchSoup.findAll('div', attrs = {'id': 'elementor-tab-content-1642'})

        # The events are built in <p> tags. We need to extract relevant information.
        elemstitle = elemst[0].find_all("p")[1].getText()
        description = elemst[0].find_all("p")[2].getText()

        # For debugging, check which <p> tags are which:
        # for tag in elemst:
        #     tdTags = tag.find_all("p")
        #     for tag in tdTags:
        #         print(tag.text)

        addr = 'N/A'# No address or time is given
        urle = elemst[0].find("a", attrs={'href': re.compile("^https://")}).get('href')

        dateRegex = re.compile(r'\d\d.\d\d.\d\d\d\d')
        datentime = dateRegex.findall(elemst[0].getText())

        dfdict = {'Date and time': datentime[0], "title": elemstitle, "location": addr, "description": description, "url": urle}
        df = pd.DataFrame(dfdict, index=[0])
        print(df)
        return df



if __name__ == "__main__":
    crawl_ahoi(url='https://ahoi.digital/aktuelle/')