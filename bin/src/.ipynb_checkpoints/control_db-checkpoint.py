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

def get_each_product_info(url):
    '''
    レビュー詳細URLから必要な情報を手に入れるコード
    SQLに紐づけて必要な部分を後から埋めるでもいいかもしれない。
    categoryの数が変動するので注意
    '''
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    review_title=soup.select('.review-title')[0].text
    star=float(re.sub('5つ星のうち','',soup.select('.a-icon-alt')[0].text))
    text=soup.select('.review-text')[0].text
    
    product_url='https://www.amazon.co.jp'+soup.select('.a-text-ellipsis > a')[0].get('href')
    category=get_category(product_url)
    
    info_list=[]
    info_list.extend([star,review_title,len(text),text])
    info_list.extend(category)
    info_list.extend(['']*(13-len(info_list)))
    
    return(tuple(info_list))

def create_pie_fig(count,label,savename):
    plt.style.use('ggplot')
    plt.rcParams.update({'font.size':18})
    #日本語対応FONT
    plt.rcParams['font.family'] = 'IPAPGothic'
    size=(8,8)
    col=cm.Spectral(np.arange(len(count))/float(len(count))) #color指定はcolormapから好みのものを。
    plt.figure(figsize=size,dpi=200)
    plt.pie(count,colors=col,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')
    plt.subplots_adjust(left=0,right=0.9)
    plt.legend(label,fancybox=True,loc='center left',bbox_to_anchor=(0.9,0.5))
    plt.axis('equal') 
    plt.savefig(savename,bbox_inches='tight',pad_inches=0.05)