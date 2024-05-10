"""
This is a boilerplate pipeline 'aquisition'
generated using Kedro 0.19.3
"""


import requests
from bs4 import BeautifulSoup

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates

#import yfinance as yf


month_dict = { 'January'  : 1,
               'February' : 2,
               'March'    : 3,
               'April'    : 4,
               'May'      : 5,
               'June'     : 6,
               'July'     : 7,
               'August'   : 8,
               'September': 9,
               'October'  : 10,
               'November' : 11,
               'December' : 12  }

def get_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # run browser in headless mode
    driver = webdriver.Chrome(service=ChromeService( ChromeDriverManager().install() ),
                              options=options) 
    return driver
    


def westmetall_download(page_url = 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash'):
    driver = get_selenium_driver()
    driver.get(page_url)

    # find tbody of table to be parsed
    elements = driver.find_elements(By.TAG_NAME, 'tbody')
    
    # count number of elements containing data
    cnt = 0
    for elem in elements:
        for line in elem.text.split('\n'):
            if ('LME' in line):
                continue
            cnt += 1
    
    dates     = np.empty(cnt, dtype=datetime.datetime)
    lme_cash  = np.empty(cnt, dtype=np.float64)
    lme_3m    = np.empty(cnt, dtype=np.float64)
    lme_stock = np.empty(cnt, dtype=np.float64)
    
    cnt = 0
    for elem in elements:
        for line in elem.text.split('\n'):
            if ('LME' in line):
                continue
            words = line.split(' ')
            
            day   = int(words[0][:-1])
            month = month_dict[words[1]]
            year  = int(words[2])
            date  = datetime.datetime(year, month, day)
            
            try:
                value_cash  = float( words[3].replace(',','') )
            except ValueError:
                value_cash = np.nan
            try:
                value_3m    = float( words[4].replace(',','') )
            except ValueError:
                value_3m = np.nan
            try:
                value_stock = float( words[5].replace(',','') )
            except ValueError:
                value_stock = np.nan
            
            # TODO: implement verbose mode
            #print(date, value_cash, value_3m, value_stock)
            
            dates[cnt]     = date
            lme_cash[cnt]  = value_cash
            lme_3m[cnt]    = value_3m
            lme_stock[cnt] = value_stock
            cnt += 1
        #
    #
    
    return pd.DataFrame({ 'Date'      : dates,
                          'LME cash'  : lme_cash,
                          'LME 3m'    : lme_3m,
                          'LME Stock' : lme_stock })


def metalsapi_download():
    # TODO
    
    return None


def investing_download(page_url='https://www.investing.com/commodities/aluminum-historical-data'):
    driver = get_selenium_driver()
    driver.get(page_url)

    elements = driver.find_elements(By.TAG_NAME, 'tbody')

    cnt = 40
    dates    = np.empty(cnt, dtype=datetime.date)
    lme      = np.empty(cnt, dtype=np.float64)
    lme_open = np.empty(cnt, dtype=np.float64)
    lme_high = np.empty(cnt, dtype=np.float64)
    lme_low  = np.empty(cnt, dtype=np.float64)
    lme_vol  = np.empty(cnt, dtype=np.float64)

    cnt = 0
    for elem in elements:
        txt = elem.text
        if (len(txt) == 0):
            continue
        
        txt = txt.replace('K','')
        txt = txt.replace(',','')
        for line in txt.split('\n'):
            split = line.split(' ')
            if len(split) == 7:
                dates[cnt]    = datetime.datetime.strptime(split[0], "%m/%d/%Y").date()
                lme[cnt]      = float(split[1])
                lme_open[cnt] = float(split[2])
                lme_high[cnt] = float(split[3])
                lme_low[cnt]  = float(split[4])
                lme_vol[cnt]  = float(split[5])
                cnt += 1
            
    return pd.DataFrame({ 'Date'      : dates[:cnt],
                          'LME cash'  : lme[:cnt],
                          'LME open'  : lme_open[:cnt],
                          'LME high'  : lme_high[:cnt],
                          'LME low'   : lme_low[:cnt],
                          'LME vol'   : lme_vol[:cnt]   })


def investing_actualize(dataset, update):
    
    print(dataset.head())
    print(type(dataset))
    
    return dataset