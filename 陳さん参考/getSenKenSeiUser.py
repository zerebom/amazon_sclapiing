import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json
import numpy as np
import time
import datetime
import matplotlib.dates as mdates

def seperateUser(bookOBJ):
  bookCommentList   = bookOBJ['comment']
  bookTransferTrend = bookOBJ['transfer_trend']
  bookTransferTime  = datetime.datetime.strptime(
    bookOBJ['transfer_time'],
    "%B %d,  %Y"
  )

  senkensei = {}
  senkensei["aru"] = []
  senkensei["nai"] = []
  
  for comment in bookCommentList:
    if ( comment['author_id'] == 0 ):
      continue
    commentTime = datetime.datetime.strptime(comment['time'],"%B %d,  %Y")
    if ( bookTransferTime > commentTime ):
      if   ( bookTransferTrend == 'up' ):
        if  ( comment['star'] > 3.0 ):
          senkensei["aru"].append(comment['author_id'])
        elif( comment['star'] < 3.0 ):
          senkensei["nai"].append(comment['author_id'])
      elif ( bookTransferTrend == 'down' ) :
        if  ( comment['star'] > 3.0 ):
          senkensei["nai"].append(comment['author_id'])
        elif( comment['star'] < 3.0 ):
          senkensei["aru"].append(comment['author_id'])
      else :
        print('Something Error happened, the trend of a book should be up or down')

  return senkensei

def getSenkensei(selectedBookPath):
  bookFP = open(selectedBookPath,'r')
  bookOBJLIST = json.load(bookFP)
  bookFP.close()

  senkensei = {}
  senkensei["aru"] = []
  senkensei["nai"] = []

  for selectedBook in bookOBJLIST:
    bookID = selectedBook['siteID']
    
    bookOBJFP = open('./json/Selected_Book_' + bookID + '.json')
    bookOBJ   = json.load(bookOBJFP)
    bookOBJFP.close()

    addSenkensei = seperateUser( bookOBJ )

    senkensei['aru'].extend(addSenkensei['aru'])
    senkensei['nai'].extend(addSenkensei['nai'])

  userFP = open('./json/senkensei.json','w')
  json.dump(senkensei,userFP)
  userFP.close()
  return senkensei

if __name__ == '__main__' :
  senkensei = getSenkensei('./json/selected_book.json')
  print('get %d persons of senkenseiAli, while get %d persons of senkenseiNai' % (len(senkensei['aru']),len(senkensei['nai'])))
