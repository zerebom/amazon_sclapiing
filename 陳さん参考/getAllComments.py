#encoding: utf-8

import time
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import getRequestFromAmazon as req
from bs4 import BeautifulSoup
import  re

browser = webdriver.Chrome()
browser.implicitly_wait(7)

def getScrollingPage(pageurl):
  browser.get(pageurl)
  time.sleep(5)
  no_of_pagedowns = 100

  for i in range(no_of_pagedowns):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);');
    time.sleep(1)
	
  source = browser.page_source.encode()
  return source
  
def getCommentLinkFromPage(userID):
  urlPre = 'https://www.amazon.com/gp/pdp/profile/'
  pageContent = getScrollingPage(urlPre + userID)
  
  linkList = []
  soup = BeautifulSoup(pageContent,"html.parser")

  
  for review in soup.find_all('a'):
    if ( review.get("href") and re.match(r"https://www.amazon.com/gp/review/", review.get("href"))):
      linkList.append( review.get('href'))
  return linkList

def getCommentFromLink(commentLinkList,authorID,tag):
  commentList = []
  count = 0 
  for commentLink in commentLinkList:
    count += 1
    print('Get %d of %d comments ...' % (count,len( commentLinkList)))
    browser.get(commentLink)
    sleep(3)
    response = browser.page_source.encode()
    soup = BeautifulSoup(response,"html.parser")
    review_group = soup.find_all(
      name  = 'div',
      attrs = {"class": "reviewText"}
    )
    catego_group = soup.find_all(
      name  = 'div',
      attrs = {"id": "nav-subnav"}    
    )
    
    cuComment = ""
    cateName = ""
    
    for review in review_group:
      cuComment = review.text
    for catego in catego_group:
      navbarItem = catego.find_all(
        name  = 'a',
        attrs = {"class" : "nav-b"} 
      )
      for navbar in navbarItem :
        content = navbar.find_all(
          name  = 'span',
          attrs = {"class" : "nav-a-content"} 
        )
        for nav in content :
          cateName = nav.text
      
    commentList.append({
      "comment"   : cuComment,
      "authorID"  : authorID,
      "category"  : cateName,
      "tag"       : tag,
      "link"      : commentLink
    })
    '''
    print({
      "comment"   : cuComment.encode('cp950','ignore'),
      "authorID"  : authorID.encode('cp950','ignore'),
      "category"  : cateName.encode('cp950','ignore'),
      "tag"       : tag.encode('cp950','ignore'),
      "link"      : commentLink.encode('cp950','ignore')
    })
    '''
  return commentList

def getUserFromJson(jsonFilePath):
  jsonFP = open(jsonFilePath,'r')
  senkensei = json.load(jsonFP)
  jsonFP.close()
  
  return senkensei

def getAllComment(inJsonPath,outJsonPath):
  commentList = []
  userIDListDict = getUserFromJson(inJsonPath)
  
  count = 1
  for user in userIDListDict['aru']:
    print('Get %d of %d Senkensei aru users ...' % (count,len( userIDListDict['aru'])))
    commentLinkList = getCommentLinkFromPage(user)
    commentList.extend(getCommentFromLink(commentLinkList,user,'aru'))
    with open(outJsonPath,'w') as jsonFp:
      json.dump(commentList,jsonFp)
    count += 1
    
  count = 1
  for user in userIDListDict['nai']:
    print('Get %d of %d Senkensei nai users ...' % (count,len( userIDListDict['nai'])))
    commentLinkList = getCommentLinkFromPage(user)
    commentList.extend(getCommentFromLink(commentLinkList,user,'nai'))
    with open(outJsonPath,'w') as jsonFp:
      json.dump(commentList,jsonFp)
    count += 1


if __name__ == '__main__':
  getAllComment('./json/senkensei.json','./json/comments_new.json')
  #getCommentFromLink(['https://www.amazon.com/gp/review/R13DKLN8XARTPW?ref_=glimp_1rv_cl'],'AAAA','nai')













