

import requests
from bs4 import BeautifulSoup

from selenium import webdriver 
#from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import datetime
import time

from http import HTTPStatus
import requests
from requests.exceptions import HTTPError

retry_codes = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]



def get_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # run browser in headless mode
    driver = webdriver.Chrome(service=ChromeService( ChromeDriverManager().install() ),
                              options=options) 
    return driver

def request_data(url, retries=5):
    response = None
    for n in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except HTTPError as exc:
            code = exc.response.status_code
            
            if code in retry_codes:
                # retry after n seconds
                time.sleep(15)
                continue
    
    if response is not None:
        return response.json()
    else:
        raise HTTPError