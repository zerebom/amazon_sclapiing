'''
自作コード
'''

import sys
import os
import re
from robobrowser import RoboBrowser

# 認証の情報は環境変数から取得する。
# AMAZON_EMAIL = os.environ['AMAZON_EMAIL']
# AMAZON_PASSWORD = os.environ['AMAZON_PASSWORD']

# RoboBrowserオブジェクトを作成する。
browser = RoboBrowser(
    parser='html.parser',  # Beautiful Soupで使用するパーサーを指定する。
    # Cookieが使用できないと表示されてログインできない問題を回避するため、
    # 通常のブラウザーのUser-Agent（ここではFirefoxのもの）を使う。
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0')


def main():
    # 注文履歴のページを開く。
    print('Navigating...', file=sys.stderr)
 
    # browser.open('https://www.amazon.co.jp/gp/product/4873116554/ref=s9_acsd_simh_hd_bw_b1x4K_c_x_3_w?pf_rd_m=AN1VRQENFRJN5&pf_rd_s=merchandised-search-4&pf_rd_r=GGPKJ52QZZAWFHSKR0RF&pf_rd_t=101&pf_rd_p=84c28d47-4e2f-5adb-b380-a7b7809ae8ee&pf_rd_i=465392')
    browser.open('https://www.amazon.co.jp/Python%E3%81%AB%E3%82%88%E3%82%8B%E3%83%87%E3%83%BC%E3%82%BF%E5%88%86%E6%9E%90%E5%85%A5%E9%96%80-%E2%80%95NumPy%E3%80%81pandas%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E3%83%87%E3%83%BC%E3%82%BF%E5%87%A6%E7%90%86-Wes-McKinney/product-reviews/4873116554/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1')


    # ページャーをたどる。
    while True:
        assert 'Python' in browser.parsed.title.string  # 注文履歴画面が表示されていることを確認する。
        print(browser.parsed.title.string)
        # print(browser.parsed.prettify())
        print_order_history()


        link_to_next = browser.get_link('次へ')  # 「次へ」というテキストを持つリンクを取得する。
        if not link_to_next:
            break  # 「次へ」のリンクがない場合はループを抜けて終了する。

        print('Following link to next page...', file=sys.stderr)
        browser.follow_link(link_to_next)  # 「次へ」というリンクをたどる。


def print_order_history():
    """
    現在のページのすべての注文履歴を表示する。
    """
    # ページ内のすべての注文履歴について反復する。ブラウザーの開発者ツールでclass属性の値を確認できる。
    for line_item in browser.select('.celwidget'):
        for column in line_item.select('.review-text'):
            print(type(column)
            
            print()
            # value_element = column.select_one('.value')


        # order = {}  # 注文の情報を格納するためのdict。
        # # 注文の情報のすべての列について反復する。
        # for column in line_item.select('.a-column'):
        #     label_element = column.select_one('.label')
        #     value_element = column.select_one('.value')
        #     # ラベルと値がない列は無視する。
        #     if label_element and value_element:
        #         label = label_element.get_text().strip()
        #         value = value_element.get_text().strip()
        #         order[label] = value  # 注文の情報を格納する。


if __name__ == '__main__':
    main()
