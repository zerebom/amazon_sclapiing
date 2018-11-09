import re
import requests
#from mybook import Book,Comment
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import randint

from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def requestAmazon(url,broswer):
  if ( os.name == 'nt' ) :
    browser.get(url)
    sleep(3)
    response = browser.page_source
  else:
    get_page  = []
    session   = requests.Session()
    ua = UserAgent()


    sleep_time = randint(5,30)
    print( "Get Amazon: Initial Sleeping, Sleep Time = %6d" % sleep_time , flush=True)
    sleep( sleep_time )
    source = session.get(url=url,headers={'User-Agent' : ua.chrome})
    sleep_min = 30
    while ( source.status_code != 200 ) :
      print(source ,  flush=True)
      sleep_time = randint(sleep_min,sleep_min * 2)
      print( "Get Amazon: Bad response sleeping, Sleep Time = %6d" % sleep_time ,  flush=True)
      sleep( sleep_time )
      source = session.get(url=url,headers={'User-Agent' : ua.chrome})
      sleep_min = int( sleep_min * 1.2 )
      
    response = source.content

  return response






