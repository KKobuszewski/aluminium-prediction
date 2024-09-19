"""
This is a boilerplate pipeline 'aquisition'
generated using Kedro 0.19.3
"""

from selenium.webdriver.common.by import By

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates

import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots

#import yfinance as yf

from aluminium_prediction import timeutils, scrapping





def westmetall_download(page_url: str = 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash',
                        all: bool = False) -> pd.DataFrame:
    """_summary_

    NOTE: This function can be used to get whole dataset from the url (data are set statically in the html).
    
    Args:
        page_url (str, optional): _description_. Defaults to 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash'.
        all (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    driver = scrapping.get_selenium_driver()
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
            month = timeutils.month_dict[words[1]]
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

def westmetall_actualize(dataset: pd.DataFrame,
                         update: pd.DataFrame) -> pd.DataFrame:
    # convert to proper datetime object
    #dataset['Date'] = dataset['Date'].apply(lambda x: datetime.date( *map(int,x.split('-')) ))
    dataset['Date'] = timeutils.convert_to_datetime(dataset['Date'])
           
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


def dataset_actualize(dataset: pd.DataFrame,
                      update: pd.DataFrame) -> pd.DataFrame:
    # convert to proper datetime object (NOTE: while saving to csv date is converted to str)
    dataset['Date'] = timeutils.convert_to_datetime(dataset['Date'])
           
    if type(dataset['Date'][0]) != type(update['Date'][0]):
        print( type(dataset['Date'][0]) )
        print( type(update['Date'][0]) )
        raise ValueError
    
    new_dataset = pd.concat([dataset, update])
    new_dataset = new_dataset.sort_values('Date')
    new_dataset = new_dataset.drop_duplicates()
    
    return new_dataset


def metals_api_convert_price(price: float) -> float:
    """_summary_
    This function converts price in USD per troy ounce to normal units...
    
    Args:
        price (float): _description_

    Returns:
        _type_: _description_
    """
    return (1.0/price)/31.1035*1000000

def metalsapi_download():
    # TODO
    
    return None


def investing_download(page_url: str = 'https://www.investing.com/commodities/aluminum-historical-data'):
    """_summary_

    NOTE: This function cannot be used to download whole dataset from the url.
    
    Args:
        page_url (str, optional): _description_. Defaults to 'https://www.investing.com/commodities/aluminum-historical-data'.

    Returns:
        _type_: _description_
    """
    driver = scrapping.get_selenium_driver()
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
            if len(split) == 9:
                dates[cnt]    = datetime.datetime.strptime('/'.join(split[:3]), "%b/%d/%Y").date()
                lme[cnt]      = float(split[3])
                lme_open[cnt] = float(split[4])
                lme_high[cnt] = float(split[5])
                lme_low[cnt]  = float(split[6])
                lme_vol[cnt]  = float(split[7])
                cnt += 1
    
    print(pd.DataFrame({ 'Date'      : dates[:cnt],
                          'LME 3m'  : lme[:cnt],
                          'LME open'  : lme_open[:cnt],
                          'LME high'  : lme_high[:cnt],
                          'LME low'   : lme_low[:cnt],
                          'LME vol'   : lme_vol[:cnt]   }))
    
    return pd.DataFrame({ 'Date'      : dates[:cnt],
                          'LME 3m'  : lme[:cnt],
                          'LME open'  : lme_open[:cnt],
                          'LME high'  : lme_high[:cnt],
                          'LME low'   : lme_low[:cnt],
                          'LME vol'   : lme_vol[:cnt]   })


def investing_actualize(dataset: pd.DataFrame,
                         update: pd.DataFrame) -> pd.DataFrame:
    # convert to proper datetime object
    #dataset['Date'] = dataset['Date'].apply(lambda x: datetime.date( *map(int,x.split('-')) ))
    dataset['Date'] = timeutils.convert_to_datetime(dataset['Date'])
    
    
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
    print(new_dataset.tail(40))
    
    return new_dataset


def investing_correct_volumes(dataset: pd.DataFrame) -> pd.DataFrame:
    dataset['Date'] = timeutils.convert_to_datetime(dataset['Date'])
    
    idx = (dataset['Date'] > datetime.date(2019, 9, 20)) & (dataset['Date'] < datetime.date(2020, 7, 4))
    dataset['LME vol'] = dataset['LME vol']*idx.astype(float)*0.1
    
    return dataset
    


def visualize_aluminium_datasets(westmetall_dataset: pd.DataFrame, 
                                 investing_dataset: pd.DataFrame):
    westmetall_dataset['Date'] = timeutils.convert_to_datetime(westmetall_dataset['Date'])
    investing_dataset['Date'] = timeutils.convert_to_datetime(investing_dataset['Date'])
    
    fig, axes = plt.subplots(ncols=1, nrows=2, sharex=True, figsize=[20.,14.])
    ax1, ax2 = axes.ravel()
    fig.suptitle('Aluminium LME 3-month prices')
    
    # LME price plot
    ax1.grid(True)
    ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax1.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME 3m'], color='k', s=0.5, alpha=0.75, label='investing.com')
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME open'], color='k', s=0.5, alpha=0.5)
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME high'], color='k', s=0.5, alpha=0.5)
    ax1.scatter(investing_dataset['Date'], investing_dataset['LME low'], color='k', s=0.5, alpha=0.5)
    
    ax1.scatter(westmetall_dataset['Date'], westmetall_dataset['LME 3m'], color='r', s=0.5, alpha=0.75, label='westmetall.com')
    ax1.legend()
    
    
    # LME Volume plot
    ax2.grid(True)
    ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    ax2.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())
    ax2.scatter(investing_dataset['Date'], investing_dataset['LME vol'], color='k', s=0.5, label='investing.com volume')
    ax2.scatter(westmetall_dataset['Date'], westmetall_dataset['LME Stock']/10000.0, color='r', s=0.5, label='westmetall.com stock')
    ax2.legend()
    
    fig.tight_layout()
    
    return fig


def plotly_aluminium_datasets( westmetall_dataset: pd.DataFrame,
                               investing_dataset: pd.DataFrame,
                               metalsapi_dataset: pd.DataFrame ):
    """_summary_

    ```
    poetry run kedro run --from-nodes "plotly_aluminium_node"
    ```
    
    Args:
        westmetall_dataset (pd.DataFrame): _description_
        investing_dataset (pd.DataFrame): _description_
        metalsapi_dataset (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    westmetall_dataset['Date'] = timeutils.convert_to_datetime(westmetall_dataset['Date'])
    investing_dataset['Date']  = timeutils.convert_to_datetime(investing_dataset['Date'])
    metalsapi_dataset['Date']  = timeutils.convert_to_datetime(metalsapi_dataset['Date'])
    
    fig = plotly.subplots.make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
            [{"type": "scatter"}],
            [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Table(header=dict(values=[k.replace(' ','<br>') for k in investing_dataset.columns[:]],
                             font=dict(size=10), align="left"),
                 cells=dict(values=[investing_dataset[k].tolist() for k in investing_dataset.columns[:]],
                             align="left")
        ), row=1, col=1,
    )
    fig.add_trace( go.Scatter( x = investing_dataset["Date"],
                               y = investing_dataset["LME vol"],
                               name = "Volume",
                               line_color='#0000ff'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Candlestick(x    = investing_dataset['Date'],
                       open = investing_dataset['LME open'],
                       high = investing_dataset['LME high'],
                       low  = investing_dataset['LME low'],
                       close= investing_dataset['LME 3m'],
                       name = 'investing.com'),
        row=3, col=1,
    )
    fig.add_trace(go.Scatter( x = westmetall_dataset['Date'],
                              y = westmetall_dataset['LME 3m'],
                              name = 'westmetall.com' ),
                  row=3, col=1
    )
    #print([*metalsapi_dataset])
    for colname in [*metalsapi_dataset][1:]:
        fig.add_trace(go.Scatter( x = metalsapi_dataset['Date'],
                                  y = metalsapi_dataset[colname],
                                  name = colname ),
                      row=3, col=1)
    print()
    
    fig.update_layout(
        height=1200,
        showlegend=True,
        title_text="<i><b>LME 3-month prices & volumes</b></i>",
    )

    #fig.write_html("LME_prices_volumes.html")
    #fig.show()
    
    return fig




def plotly_aluminium_prices( westmetall_dataset : pd.DataFrame,
                               investing_dataset: pd.DataFrame,
                               metalsapi_dataset: pd.DataFrame ):
    """_summary_

    ```
    poetry run kedro run --from-nodes "plotly_aluminium_node"
    ```
    
    Args:
        westmetall_dataset (pd.DataFrame): _description_
        investing_dataset (pd.DataFrame): _description_
        metalsapi_dataset (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    westmetall_dataset['Date'] = timeutils.convert_to_datetime(westmetall_dataset['Date'])
    investing_dataset['Date']  = timeutils.convert_to_datetime(investing_dataset['Date'])
    metalsapi_dataset['Date']  = timeutils.convert_to_datetime(metalsapi_dataset['Date'])
    
    # create plot
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x    = investing_dataset['Date'],
                                 open = investing_dataset['LME open'],
                                 high = investing_dataset['LME high'],
                                 low  = investing_dataset['LME low'],
                                 close= investing_dataset['LME 3m'],
                                 name = 'investing.com'))
    fig.add_trace(go.Scatter( x = westmetall_dataset['Date'],
                              y = westmetall_dataset['LME 3m'],
                              name = 'westmetall.com' ))
    for colname in [*metalsapi_dataset][1:]:
        fig.add_trace(go.Scatter( x = metalsapi_dataset['Date'],
                                  y = metalsapi_dataset[colname],
                                  name = colname ))
    print()
    
    fig.update_layout(
        xaxis_range = [datetime.date(2009,1,1),datetime.datetime.today()],
        yaxis_range = [1000,3500],
        height=1200,
        showlegend=True,
        title_text="<i><b>LME 3-month prices & volumes</b></i>",
    )
    
    return fig  