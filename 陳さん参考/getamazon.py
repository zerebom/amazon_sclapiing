import re
import requests
import json
import getRequestFromAmazon
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import randint
from time import sleep

def startRequest(book):
  prefix    = 'https://www.amazon.com/product-reviews/'
  pre_page  = '/ref=cm_cr_arp_d_viewopt_sr?filterByStar=all_stars&pageNumber='
  post_page = '&sortBy=recent&reviewerType=all_reviews'
  get_page  = []
  session   = requests.Session()
  ua = UserAgent()

  for comment_page in range(1 , book['comment_page_num'] + 1 ) :
    get_page.append( prefix + book['siteID'] + pre_page + str(comment_page) + post_page )

  for url in get_page:
    response = getRequestFromAmazon.requestAmazon(url)
    soup = BeautifulSoup(response,"html.parser")
    review_group = soup.find_all(
      name  = 'div',
      attrs = {"data-hook": "review"}
    )
    for review in review_group :
      cuReview = {}
      div_group = review.find_all('div')

      # star
      result  =   re.search(r'(\d+\.\d+\s+)out of 5 stars',div_group[0].a.i.text) 
      cuReview['star']    =   float(result.group(1))
      
      if ( hasattr(div_group[1].span,'a') and hasattr(div_group[1].span.a,'text') ):
        # Author
        cuReview['author']  =   div_group[1].span.a.text 
        
        # Author ID
        result  =   re.search(r'profile/(\w+)\s?',div_group[1].span.a['href'])
        cuReview['author_id'] = result.group(1)
      else :
        # Default ID and author
        cuReview['author']    = 'null' 
        cuReview['author_id'] = 0


      
      # Time
      result  =   re.search(
                    r'on\s?([\w, ]+)',
                    div_group[1].span.next_sibling.next_sibling.next_sibling.text
                  )
      cuReview['time']    = result.group(1)
      
      # Review
      str_gp = div_group[3].span.strings
      comment = ''
      for st in str_gp:  
        comment += st + "\n"
      cuReview['comment'] = comment

      # Write into Book
      book['comment'].append(cuReview)
      del cuReview

  bookFile = open('./json/Selected_Book_' +book['siteID'] +'.json' , 'w')
  bookJSON = json.dump(book,bookFile)
  bookFile.close()

if __name__ == '__main__':
  book_list = []
  file = open('./json/selected_book.json','r')
  book_list = json.load(file)
  file.close()
  for book in book_list:
    bookToGet = {} 
    bookToGet['siteID'] = book['siteID']
    bookToGet['book_name'] = book['book_name']
    bookToGet['comment_page_num'] = book['comment_page_num']
    bookToGet["transfer_time"] = book["transfer_time"]
    bookToGet["transfer_trend"] = book["transfer_trend"]
    bookToGet['comment'] =  []

    print( bookToGet ) 
    startRequest(bookToGet)











