import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import pdb 
import json
import numpy as np
import time
import random
import datetime
import matplotlib.dates as mdates
import nltk
from nltk.corpus import stopwords
import treetaggerwrapper
import sys
import csv
import pickle
import os.path
from sklearn.cross_validation import train_test_split
from sklearn.utils import shuffle
from klepto.archives import dir_archive

DEBUG = True

def makeUserComment(userlistFile):
  with open(userlistFile,'r') as fp :
    if(DEBUG == True) :
      print("=====Reading wordList file====")
    userlist    = json.load(fp)  

  CVNumber     = 5
  minWordsNum  = 100
  maxWordPerPerson = {'aru' : 2000 , 'nai' : 1200}
  maxWordPerReview = 100

  
  cvGroup  = []
  userKeys = shuffle(list(userlist.keys()))
  for i in range(CVNumber):
    indexStart = int( (i/CVNumber)*len(userKeys)   )
    indexEnd   = int( ((i+1)/CVNumber)*len(userKeys) )
    test_set   = []
    train_set  = []
    arunaiNum  = {'aru' : 0 , 'nai' : 0}
    for userIndex in range(len(userKeys)):
      newComment = []
      wordCount  = 0
      user       = userKeys[userIndex]
      randomword = shuffle(userlist[user]['word'])

      if ( userlist[user]["wordNum"] < minWordsNum ):
        continue 
        
      for j in range( min( userlist[user]["wordNum"] , maxWordPerPerson[userlist[user]['tag']] ) ):
      
        newComment.append(randomword[j][2])
        wordCount += 1
        
        if ( wordCount % maxWordPerReview == 0 ):
          if ( indexStart <= userIndex and userIndex < indexEnd ):
            # Test Data 
            test_set.append( {'comment' : newComment , 'tag' : userlist[user]['tag'] } )
            arunaiNum[userlist[user]['tag']] += 1
          else :
            # Train Data
            train_set.append( {'comment' : newComment , 'tag' : userlist[user]['tag'] } )
            
          newComment = []
          
          
    print(arunaiNum)
    cvGroup.append( {'train' : train_set , 'test' : test_set} )
  
  return cvGroup

def findWord(commentFileName,word,tag):
  with open(commentFileName,'r') as fp :
    commentFile = json.load(fp)
  
  authorCount = {}
  for comment in commentFile :
    if ( comment['comment'].lower().find(word) >= 0 and tag == comment['tag'] ):
      print(comment['comment'].encode('cp950','ignore'))
      print("------------------------------------------")
      print(comment['authorID'].encode('cp950','ignore'))
      print("------------------------------------------")
      if(not comment['authorID'] in authorCount):
        authorCount[comment['authorID']] = True
  print("---------------------")
  print("Total Author = %d" %(len( list( authorCount.keys() ) ) ) )
  print("---------------------")
  
def soseiAnalyze(commentFileName,userlistFile):
  # Setting
  
  cvData  = makeUserComment(userlistFile)
  partitionRatio = 0.8
  maxiter = 20
  accuracyRecord = []
  onePersonMax   = 10
  freqMax  = 1000 
  
  for CVItt in range(len(cvData)):
    trainComment = cvData[CVItt]['train']
    testComment  = cvData[CVItt]['test']
    
    # Get most frequently words
    wordCount = {}
    count = 0 
    for comment in trainComment :
      for word in comment['comment']:
        if ( word in wordCount ) :
          wordCount[word] += 1
        else:
          wordCount[word]  = 1
      count += 1
    count    = 0 
    freqWord = {}
    for k, v in sorted(wordCount.items(), key=lambda x:x[1], reverse=True):
      freqWord[k] = v
      count += 1
      if ( count > freqMax ):
        break        
      
    
    # Making Data
    train_set = []
    test_set  = []    
    for comment in trainComment:
      feature_set = {}
      for word in freqWord:
        feature_set[word] = ( word in comment['comment'] )
      train_set.append(  (feature_set,comment["tag"]) )  
    for comment in testComment:
      feature_set = {}
      for word in freqWord:
        feature_set[word] = ( word in comment['comment'] )
      test_set.append(  (feature_set,comment["tag"]) )
    '''      
  for userID, userDict in sorted(userlist.items(), key=lambda x:x[1]["reviewNum"], reverse=True):
  
    allData        = []
    author_record  = {}
    train_set = []
    test_set  = []
    for comment in commentFile:
      if ( comment["authorID"] in author_record ) :
        if ( author_record[comment["authorID"]] >= onePersonMax ):
          continue
        else:
          author_record[comment["authorID"]] += 1
      else:
        author_record[comment["authorID"]]  = 1  
      feature_set = {}
      for word in freqWord:
        feature_set[word] = ( word in comment['comment'] )
      if ( comment["authorID"] == userID ):
        test_set.append(  (feature_set,comment["tag"]) )
      else:
        train_set.append( (feature_set,comment["tag"]) )
    '''
    print("TRAIN = %9d , TEST = %9d " %(len(train_set),len(test_set)))
    print("Start Traning") 
    maxentclassifier = nltk.MaxentClassifier.train(shuffle(train_set),algorithm='gis',max_iter=maxiter)
    print ("MaxentClassifier Prediction")
    accuracyRecord.append( [
      CVItt,
      nltk.classify.accuracy(maxentclassifier,shuffle(test_set))  
    ] )
    print ("Acc Rate = %6.3f" %(accuracyRecord[-1][1]) )
    
    avg = 0
    for acc in accuracyRecord:
      avg += acc[1]
    avg /= len(cvData)
    print("avg acc = %10.5f" %(avg))
    '''
    with open('./csv/cvCAccRec.csv', 'w') as fp:
      writer = csv.writer(fp, lineterminator='\n') 
      for acc in accuracyRecord :
        writer.writerow( [acc[0],acc[1]] )
    
    print ("Informative feature")
    print (maxentclassifier.show_most_informative_features(300))
    break
    '''
def wordSplit(sentence):
  stopset = set(stopwords.words('english'))
  tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='C:\\TreeTagger')
  tags = tagger.TagText(sentence)
  tags = [ x.split("\t") for x in tags ]
  filteredWord = []
  for taggedWord in tags :
    if ( len(taggedWord)  < 3 or taggedWord[2] in stopset or len(taggedWord[2])  < 3 ) :
      continue  

    if ( taggedWord[2] == 'replaced-dns' or
         taggedWord[2] == '@card@' or 
         taggedWord[2] == "n't" 
    ):
      continue
      
    filteredWord.append( taggedWord )    

  return filteredWord

def userStats(commentList):
  count = 0 
  userlist = {}
  for comment in commentList :
    if ( comment["authorID"] in userlist ):
      if ( not (comment["category"] == "Books" or comment["category"] == "Kindle books") ):
        continue
      if ( comment["authorID"] in userlist ):
        userlist[comment["authorID"]]["reviewNum"] += 1
        userlist[comment["authorID"]]["word"].extend(wordSplit(comment["comment"]))
        userlist[comment["authorID"]]["wordNum"]   = len(userlist[comment["authorID"]]["word"])
    else :
      userDict = {}
      userDict["reviewNum"]  = 1
      userDict["word"] = wordSplit(comment["comment"])
      userDict["wordNum"]    = len(userDict["word"])
      userDict["tag"]  = comment["tag"]
      userlist[comment["authorID"]] = userDict
    
    
    count += 1
    if ( count % 50 == 0 ):
      print ( "Handle %d of %d" %(count,len(commentList) ) ) 
      
  #if(DEBUG == True) :
    #print("=====userlist====")
    #print(userlist)
  return userlist

def cateStats(commentList):
  catelist = {}
  for comment in commentList :
    if ( comment["category"] in catelist ):
      catelist[comment["category"]][0] += 1
    else :
      catelist[comment["category"]]  = [1,0,0]
    if ( comment["tag"]  == 'aru' ):
      catelist[comment["category"]][1]  += 1
    elif( comment["tag"] == 'nai' ):
      catelist[comment["category"]][2]  += 1
  if(DEBUG == True) :
    for cate,num in sorted(catelist.items(), key=lambda x: x[1][0],reverse=True) :
      print("%30s => %5d %5d %5d" %(cate,num[0],num[1],num[2]) )
  return catelist
  
def analyzeComments(filename):
  with open(filename,'r') as fp :
    if(DEBUG == True) :
      print("=====Reading comments file====")
    commentList = json.load(fp)
  
  userlist = userStats(commentList)
  with open('./csv/analyze.csv', 'w') as fp:
    writer = csv.writer(fp, lineterminator='\n') 
    for userID, userDict in sorted(userlist.items(), key=lambda x:x[1]["wordNum"], reverse=True):
      writer.writerow( [userID,userDict["wordNum"],userDict["reviewNum"],userDict["tag"]] )      
  with open('./json/userList.json','w') as fp :
    json.dump(userlist,fp)
    
def makeLearningData(userlistFile):
  with open(userlistFile,'r') as fp :
    if(DEBUG == True) :
      print("=====Reading wordList file====")
    userlist    = json.load(fp)
    
  wordCount      = {'aru' : 0  , 'nai' : 0}
  wordTotal      = {'aru' : 0  , 'nai' : 0}
  wordTruncate   = {'aru' : 5000 , 'nai' : 1500}
  newComment     = {'aru' : {"comment" : [] ,"tag" : "aru"} , 'nai' : {"comment" : [] ,"tag" : "nai" } }
  newCommentList = []
  
  for userID, userDict in sorted(userlist.items(), key=lambda x:x[1]["wordNum"], reverse=False):
    tag = userDict['tag']
    sameAuthorCount = 0 
    for word in userDict["word"]:
      if ( sameAuthorCount ==  wordTruncate[tag] ):
        break 
      newComment[tag]["comment"].append(word[2])
      wordCount[tag]  += 1
      wordTotal[tag]  += 1
      sameAuthorCount += 1
      if( wordCount[tag] == wordTruncate[tag] ) :
        newCommentList.append(newComment[tag])
        newComment[tag] = {"comment" : [] ,"tag" : tag }
        wordCount[tag]  = 0
  return newCommentList
  
if __name__ == '__main__' :
  #analyzeComments('./json/comments_new.json')
  #makeUserComment('./json/userList.json')
  soseiAnalyze('./json/comments_new.json','./json/userList.json')
  #makeLearningData('./json/userList.json')
  #statsic = soseiAnalyze('./json/comments_new.json')
  #findWord('./json/comments_new.json','violence','nai')


  #preHandle("Save the time of the reader.")
  
'''
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
'''

