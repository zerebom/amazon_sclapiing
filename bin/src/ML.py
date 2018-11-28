import pandas as pd 
import numpy as np
import sklearn
import seaborn as sns
# import matplotlib as plt
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score

# def preproDF(df,PERCENT):
#     df['kouseihi']=df['sum']/df['sum'].sum()
#     df['ruisekihi']=df['sum'].cumsum()/df['sum'].sum()
#     df=df.reset_index(drop=True)
#     df=df[df['kouseihi']>PERCENT]
    
#     df=df.T
#     wordcouttdf=df[['Unnamed: 0','sum_word','kouseihi','ruisekihi']]
#     df.drop(columns=['Unnamed: 0','sum_word','kouseihi','ruisekihi'],inplace=True)
#     return(df,wordcouttdf)


def preproDF(df,PERCENT):
    df['kouseihi']=df['sum']/df['sum'].sum()
    df['ruisekihi']=df['sum'].cumsum()/df['sum'].sum()
    df=df.reset_index(drop=True)
    df=df[df['kouseihi']>PERCENT]
    # print(df.columns)
    df=df.fillna(0)
    wordcouttdf=df[['Unnamed: 0','sum','kouseihi','ruisekihi']]
    df.drop(columns=['Unnamed: 0','sum','kouseihi','ruisekihi'],inplace=True)
    df=df.T
    wordcouttdf=wordcouttdf.T
    
    return(df,wordcouttdf)


