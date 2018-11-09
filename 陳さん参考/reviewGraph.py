import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import json
import numpy as np
import time
import datetime
import matplotlib.dates as mdates

def drawReview(bookPath):
  bookFP = open(bookPath,'r')
  bookOBJ = json.load(bookFP)
  bookFP.close()

  bookTitle = bookOBJ['book_name']
  bookCommentList = bookOBJ['comment']
  bookID = bookOBJ['siteID']   
  commentRecord =  []
  timeRecord = []
  for comment in bookCommentList:
    commentRecord.append( comment['star'] )
    timeRecord.append( datetime.datetime.strptime(comment['time'],"%B %d,  %Y"))

  commentRecord = commentRecord[::-1]
  timeRecord = timeRecord[::-1]
  commentLen = len(commentRecord)
  #aveWeighted = np.ones(5)/5.0
  
  #moving_average = np.convolve(commentRecord,aveWeighted,'valid')
  fig = plt.figure(figsize=(12,7),dpi=100)
  ax  = fig.add_subplot(1,1,1)
  ax.plot(timeRecord,commentRecord,'o',markersize=4)
  ax.set_xlabel("Time")
  ax.set_ylabel("Stars")
  ax.set_title(bookTitle)

  ax.set_ylim(-0.5,5.5)
  ax.grid()
  days = mdates.AutoDateLocator()
  daysFmt = mdates.DateFormatter("%Y-%m")
  ax.xaxis.set_major_locator(days)
  ax.xaxis.set_major_formatter(daysFmt)
  plt.savefig( bookID +'.png')
  plt.close()

if __name__ == '__main__' :
  book_list = []
  file = open('./json/selected_book.json','r')
  book_list = json.load(file)
  file.close()
  for book in book_list:
    drawReview( book['siteID'] + '.json' )
