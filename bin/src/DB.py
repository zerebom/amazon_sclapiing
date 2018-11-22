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
        if i>=start_num:
            print(f'{i}人目、{row[0]}さんのレビューを取得中です')
            product_url,product_name=scroll_and_get_100_Products_url('https://www.amazon.co.jp'+row[2])
            name_list=[row[0]]*len(product_url)
            rate_list=[row[1]]*len(product_url)
            id_=[x for x in range(1,len(product_url)+1)]
            datas=[(n,i,r,p,pn) for n,i,r,p,pn in zip(name_list,id_,rate_list,product_url,product_name)]

            insert_sql = 'insert into products (name,id,rate,url,pn) values (?,?,?,?,?)'
            #↑順番が違う
            Wc.executemany(insert_sql, datas)
            Wconn.commit()

def helper_get_producu_url(browser):
    '''
    scroll_and_get_100_Products_urlの中で同じような表記が繰り返されるので、それを書き出した。
    具体的にはURLを取得してHTMLを取得する部分
    '''
    # browser.get(url)
    # time.sleep(0.3) 
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    try:
        review_number=soup.select('.dashboard-desktop-stat-value')[1].text
    except:
        review_number=9999999999
    
    
    review_box=soup.select('.profile-at-card')
    def igonre_none_product(x):
        try:
            return x.select('.profile-at-product-title-container > span')[0].text
        except:
            return('no_product')

    products_name=[igonre_none_product(x) for x in review_box]
    review_url=['https://www.amazon.co.jp'+x.select('.profile-at-review-link')[0].get('href') for x in review_box]
    
    return(browser,review_number,review_url,products_name)


def scroll_and_get_100_Products_url(url,max_num=300):
    '''
    レビュアー詳細URLからその人の全レビューURLを取得するコード
    その人の獲得した星の数や、レビュー数もその気になれば手に入れられる
    デフォルトでは100件以上は収集しない
    '''
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    time.sleep(0.1)
    browser,review_number,review_url,products_name=helper_get_producu_url(browser)[0:4]
    print(f'総レビュー数:{review_number}件')
    i=0

    #レビュー数とURL数が一致する場合終わる
    while(int(review_number)!=len(review_url)):
        review_url=helper_get_producu_url(browser)[2]
        i+=1
        print(f'{i}回目のループ')
        if(len(review_url)>=max_num):
            break
        
        #最下部までスクロールするようにする
        for _ in range(0,50):
            browser.execute_script('scroll(0, document.body.scrollHeight)')
            time.sleep(0.08) 
        
        review_url2=helper_get_producu_url(browser)[2]
        print(f'{len(review_url2)}件のレビューを取得しました。')
        #変化がなければ終了
        if(len(review_url)==len(review_url2)):
            print('break!')
            break
        
       
    return(review_url,products_name)
