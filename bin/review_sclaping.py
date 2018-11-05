import sys
import os
import re
from robobrowser import RoboBrowser

browser = RoboBrowser(
    parser='html.parser',  # Beautiful Soupで使用するパーサーを指定する。
    # Cookieが使用できないと表示されてログインできない問題を回避するため、
    # 通常のブラウザーのUser-Agent（ここではFirefoxのもの）を使う。
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0')


    
