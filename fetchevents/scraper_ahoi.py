#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 22/03/2021

import requests, bs4, re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def crawl_ai(url='https://ai.hamburg/en/events/', evnum = 3): #'https://ai.hamburg/de/events/'):
    """ This is an event scraper for ahoi digital events. Inputs are the event page URL and
    the output contains a dataframe with the next event of this group. """

    # Create our driver object with the headless parameter so that the browser window doesn't open.
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Get the page and extract the WebElement
    # driver.get(url)
    # driver.implicitly_wait(5)
    # driver.find_element_by_class_name("wmpci-popup-close")
    # seq = driver.find_elements_by_tag_name('iframe')
    # print("No of frames present in the web page are: ", len(seq))
    # try:
    #     alert = driver.switch_to.alert()
    #     alert.dismiss()
    # except:
    #     print("no alert to accept")


    # Get the page and extract the clock WebElement
    driver.get(url)
    driver.implicitly_wait(5)
    element = driver.find_element_by_class_name('wmpci-popup-close')
    # element.is_displayed()

    driver.execute_script("arguments[0].click();", element)

    # actions = ActionChains(driver)
    # actions.move_to_element(element).perform()
    # driver.execute_script("arguments[0].scrollIntoView();", element)

    # Now from Selenium to Beautiful Soup
    noStarchSoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    if not noStarchSoup.select('elementor-post__card') == None:
        # get the entire event
        # elems = noStarchSoup.select('elementor-tab-content-1642')
        # print("----------------------------------------------------------------")
        elemst = noStarchSoup.findAll('div', attrs = {'class': 'card h-100'})

        df = pd.DataFrame(columns=['date', 'time', 'title', 'location', 'description', 'url'])

        # cycle over the first three events listed
        for i in range(evnum):
            # The events are built in <p> tags. We need to extract relevant information.
            title = elemst[i].find_all("h5")[0].getText()

            # Click on event card to get to Event body
            eventelem = driver.find_elements_by_class_name("card-link")[i]
            driver.implicitly_wait(5)
            driver.execute_script("arguments[0].click();", eventelem)

            # driver.execute_script("arguments[0].click();", WebDriverWait(driver, 3).until(
            #     EC.element_to_be_clickable(eventelem)))

            # driver.execute_script("arguments[0].click();", WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.CLASS_NAME, "card-link"))))
            # driver.find_elements_by_class_name('card-link')[.click()

            # Change browser window to new window after
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)

            eventSoup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            eventbody = eventSoup.findAll('div', attrs = {'class': 'caption'})

            body = ''.join([x.getText() for x in eventbody[0].find_all("p")[2:]])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            addr = 'N/A'# No address or time is given
            urle = elemst[i].find("a", attrs={'href': re.compile("^https://")}).get('href')

            # dateRegex = re.compile(r'\d\d.\d\d.\d\d\d\d')
            # datentime = dateRegex.findall(elemst[0].getText())

            from .helper import split_datetime
            date,_ = split_datetime(elemst[i].getText())
            dateRegex = re.compile(r'\d\d:\d\d')
            time = dateRegex.findall(elemst[i].getText())[0]

            df.loc[i] = [date.to_list()[0], time, title, addr, body, urle]

        driver.quit()
        print(df)
        return df



if __name__ == "__main__":
    crawl_ai(url='https://ai.hamburg/en/events/', evnum=3)