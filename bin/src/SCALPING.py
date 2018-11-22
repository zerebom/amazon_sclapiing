import urllib.request as urllib
from bs4 import BeautifulSoup
import re
from contextlib import closing
import sqlite3
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
options = Options()
options.add_argument('--headless')
 
browser = webdriver.Chrome(chrome_options=options) 


def scroll_and_get_100_Products_url(url,max_num=100):
    '''
    レビュアー詳細URLからその人の全レビューURLを取得するコード
    その人の獲得した星の数や、レビュー数もその気になれば手に入れられる
    デフォルトでは100件以上は収集しない
    '''
    browser.get(url)
    time.sleep(0.3) 
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    review_number=soup.select('.dashboard-desktop-stat-value')
    print(review_number,end='')
    review_box=soup.select('.profile-at-card')
    review_url=['https://www.amazon.co.jp'+x.select('.profile-at-review-link')[0].get('href') for x in review_box]
    i=0
    try:
        print(review_number[1].text)
    except:
        browser.execute_script('scroll(0, document.body.scrollHeight)')
        time.sleep(0.3)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        review_number=soup.select('.dashboard-desktop-stat-value')
        print(review_number)
        review_box=soup.select('.profile-at-card')
        review_url=['https://www.amazon.co.jp'+x.select('.profile-at-review-link')[0].get('href') for x in review_box]
    
    while(int(review_number[1].text)!=len(review_url)):
        i+=1
        if(len(review_url)>=100):
            break
        if i==30:
            break
        browser.execute_script('scroll(0, document.body.scrollHeight)')
        time.sleep(0.3) 
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        review_number=soup.select('.a-size-large.a-color-base')
        review_box=soup.select('.profile-at-card')
        review_url=['https://www.amazon.co.jp'+x.select('.profile-at-review-link')[0].get('href') for x in review_box]
        print(f'{len(review_url)}件のレビューを取得しました。')
    
    return(review_url)

#商品レビューURLから商品URLに行き、カテゴリーをリスト型にして持ってきてくれる
def get_category(product_url):
    '''
    product_urlから商品URL詳細URLに飛び、その後カテゴリを取得してくる
    
    return:
        category str
    '''
    browser.get(product_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    category=soup.select('.a-unordered-list')[0].text
    category=re.sub('›','',category)
    category=re.sub('\n','',category)
    
    category.split()
    return(category)