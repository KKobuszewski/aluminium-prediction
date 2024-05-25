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


def convert_to_datetime(column):
    return column.apply(lambda x: datetime.date( *map(int,x.split('-')) ))


def westmetall_download(page_url = 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash',
                        all=False):
    """_summary_

    NOTE: This function can be used to get whole dataset from the url (data are set statically in the html).
    
    Args:
        page_url (str, optional): _description_. Defaults to 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash'.
        all (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
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
    
    dates     = np.empty(cnt, dtype=datetime.date)
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
            date  = datetime.date(year, month, day)
            
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
        if all is False:
            break
    #
    
    return pd.DataFrame({ 'Date'      : dates[:cnt],
                          'LME cash'  : lme_cash[:cnt],
                          'LME 3m'    : lme_3m[:cnt],
                          'LME Stock' : lme_stock[:cnt] })

def westmetall_actualize(dataset, update):
    # convert to proper datetime object
    #dataset['Date'] = dataset['Date'].apply(lambda x: datetime.date( *map(int,x.split('-')) ))
    dataset['Date'] = convert_to_datetime(dataset['Date'])
           
    if type(dataset['Date'][0]) != type(update['Date'][0]):
        print( type(dataset['Date'][0]) )
        print( type(update['Date'][0]) )
        raise ValueError
    
    new_dataset = pd.concat([dataset, update])
    new_dataset = new_dataset.sort_values('Date')
    new_dataset = new_dataset.drop_duplicates()
    
    print()
    print(100*'-')
    print()
    print(new_dataset.head(40))
    print(new_dataset.tail(40))
    print()
    return new_dataset



def metalsapi_download():
    # TODO
    
    return None


def investing_download(page_url='https://www.investing.com/commodities/aluminum-historical-data'):
    """_summary_

    NOTE: This function cannot be used to download whole dataset from the url.
    
    Args:
        page_url (str, optional): _description_. Defaults to 'https://www.investing.com/commodities/aluminum-historical-data'.

    Returns:
        _type_: _description_
    """
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
    # convert to proper datetime object
    #dataset['Date'] = dataset['Date'].apply(lambda x: datetime.date( *map(int,x.split('-')) ))
    dataset['Date'] = convert_to_datetime(dataset['Date'])
    
    
    print(dataset.head())
    print(update.head())
    
    print( type(dataset['Date'][0]) )
    print( type(update['Date'][0]) )
    
    print()
    print(100*'-')
    print()
    
    new_dataset = pd.concat([dataset, update])
    new_dataset = new_dataset.sort_values('Date')
    new_dataset = new_dataset.drop_duplicates()
    print(new_dataset)
    #
    #print(new_dataset.head())
    print(new_dataset.tail(40))
    
    return new_dataset


def visualize_aluminium_datasets(westmetall_dataset, investing_dataset):
    westmetall_dataset['Date'] = convert_to_datetime(westmetall_dataset['Date'])
    investing_dataset['Date'] = convert_to_datetime(investing_dataset['Date'])
    
    fig, axes = plt.subplots(ncols=1, nrows=2, sharex=True, figsize=[16.,10.])
    ax1, ax2 = axes.ravel()
    
    # LME price plot
    ax1.grid(True)
    ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax1.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME cash'], color='k', s=0.5, alpha=0.75, label='investing.com')
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME open'], color='k', s=0.5, alpha=0.5)
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME high'], color='k', s=0.5, alpha=0.5)
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME low'], color='k', s=0.5, alpha=0.5)
    
    ax1.scatter(westmetall_dataset['Date'], westmetall_dataset['LME cash'], color='r', s=0.5, alpha=0.75, label='westmetall.com')
    ax1.legend()
    
    
    # LME Volume plot
    ax2.grid(True)
    ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax2.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    ax2.scatter(investing_dataset['Date'], investing_dataset['LME vol'], color='k', s=0.5, label='investing.com volume)
    ax2.scatter(westmetall_dataset['Date'], westmetall_dataset['LME Stock']/10000.0, color='r', s=0.5, label='westmetall.com stock')
    ax2.legend()
    
    fig.tight_layout()
    
    return fig
    