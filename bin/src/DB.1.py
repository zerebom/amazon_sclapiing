import urllib.request as urllib
from bs4 import BeautifulSoup
import re
from contextlib import closing
import sqlite3
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

options = Options()
options.add_argument('--headless') 
browser = webdriver.Chrome(chrome_options=options)
'''
各ユーザーの商品URLをすべて取得する
get_one_people_each_products_url>scroll_and_get_100_Products_url>helper_get_producu_url
↓
各商品のカテゴリを取得する
get_each_product_info>get_category
'''

def get_db_conn(name):
    '''
    sql文を何度も書きたくなかったので書いた
    '''
    conn=sqlite3.connect(name,isolation_level=None)
    c=conn.cursor()
    return(conn,c)

def get_category(product_url):
    browser.get(product_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    try:
        a=soup.select('.a-unordered-list')[0].text
    except:
        time.sleep(0.3)
        browser.get(product_url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    try:
        a=soup.select('.a-unordered-list')[0].text
    except:
        print('no_product')
        return(['no_product'])  
    category=soup.select('.a-unordered-list')[0].text
    category=re.sub('›','',category)
    category=re.sub('\n','',category)
    category=category.strip()
    category=category.split()
    
    return(category)
def get_one_people_each_products_url(Rconn,Rc,Wconn,Wc,select_sql,start_num=0):
    '''
    レビュワーURLを一気に受け取り、一つずつfor文を回す。
    その後一度にレビューURLを取得し、新しいDBに格納する
    各行にそのレビュアーの名前・商品名（NEW)・バカの壁につけた星・商品URLを記録する
    Parameters
    ------------------
    Rconn,Rc:読み込むDBのコントローラー。レビュワーURLが格納されているDB
    Wconn,Wc:書き出すDBのコントローラー。プロダクトURLが格納される予定のDB
    select_sql:読み込むDBにどんな指示をだすか。例えば星4以上のレビュアーのみに絞るなど
    '''
    
    for i,row in enumerate(Rc.execute(select_sql)):
        if i<=start_num:
            continue
        
        print(f'{i}人目、{row[0]}さんのレビューを取得中です')
        
        browser.get('https://www.amazon.co.jp'+row[2])
        product_url,product_name=get_product_url(browser,max_url=500)
        id_=[x for x in range(1,len(product_url)+1)]
        datas=[(n,i,r,pu,pn) for n,i,r,pu,pn in zip([row[0]]*len(product_url),id_,[row[1]]*len(product_url),product_url,product_name)]

        insert_sql = 'insert into products (name,id,rate,url,pn) values (?,?,?,?,?)'
        #↑順番が違う
        Wc.executemany(insert_sql, datas)
        Wconn.commit()


def get_product_url(browser,max_url):
    '''
    URLを取得してHTMLを取得する部分
    '''
    '''-------------------------------------------------------------------'''
    lenurl=0
    break_power=0

    def igonre_none_product(x):
        try:
            return x.select('.profile-at-product-title-container > span')[0].text
        except:
            return('no_product')
    '''-------------------------------------------------------------------'''
    soup = BeautifulSoup(browser.page_source, "lxml")
    try:
        review_number=soup.select('.dashboard-desktop-stat-value')[1].text
    except:
        review_number=999999
    print(f'レビューの数は{review_number}。')
    
    
    
    while lenurl<=max_url:
        browser.execute_script('scroll(0, document.body.scrollHeight)')
        soup = BeautifulSoup(browser.page_source, "lxml")
        review_box=soup.select('.profile-at-card')
        review_url=['https://www.amazon.co.jp'+x.select('.profile-at-review-link')[0].get('href') for x in review_box]
        products_name=[igonre_none_product(x) for x in review_box]    
        lenurl2=len(review_url)
        
        if lenurl+10==lenurl2:
            break_power=0
            
        if lenurl==lenurl2:
            break_power+=1
        
        lenurl=lenurl2
        
        if break_power>=5:
            print('Break!')
            return(review_url,products_name)

        print(len(review_url),end='|')
    
    return(review_url,products_name)
