import glob
import re
import pandas as pd
import MeCab
from collections import Counter

def make_stopword():
    f = open(r"C:\Users\icech\Desktop\share\Lab\2018_09_05\Docments\stopword.txt","r")
    list = []
    for x in f:
        list.append(x.rstrip("\n"))
    f.close()
    return(list)

def make_lines(txt,Flg_matubi=False):
    for sentence in txt:
        if Flg_matubi==True:
            sentence=re.sub('.+、','',sentence)
        morphemes = []
        #Note PCのばあいこっち↓
        # mecab = MeCab.Tagger(r'-d C:\Users\icech\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20180625')
        
        mecab = MeCab.Tagger(r'-d C:\Users\k-higuchi\mecab-ipadic-neologd\build\mecab-ipadic-2.7.0-20070801-neologd-20181112')
        #Lab PCのばあいこっち↑
        
        wakatis=mecab.parse(sentence)
        wakatis=wakatis.split('\n')
        for wakati in wakatis:
            if wakati=='EOS'or'':
                yield morphemes
                break
                
            cols = wakati.split('\t')
            res_cols = cols[1].split(',')
            morpheme = {
            'surface': cols[0],
            'base': res_cols[6],
            'pos': res_cols[0]}
            morphemes.append(morpheme)

def clean_txt(fname):
    with open(fname,errors='ignore') as data_file:
        text_data=data_file.read()
        text_data=re.sub('\（.+\）','',text_data)
        text_data=re.sub('.+　','',text_data)
        text_data=re.sub('\n','',text_data)
        text_data=re.sub('\\u3000','',text_data)
        text_data=text_data.split('。')
        return(text_data)

def count_morpheme(txt,word_class='動詞',stop_IO=False):
    word_counter = Counter()
    stopword=make_stopword()

    for morphemes in make_lines(txt,Flg_matubi=False):
        for morpheme in morphemes:
            if stop_IO==True:
                if len(morpheme['base'])==1 or morpheme['base'] in stopword:
                    continue
            else:
                if len(morpheme['base'])==1:
                    continue

            if morpheme['pos'] == word_class:
                word_counter.update([morpheme['base']])
    return(word_counter)
    
def count_matubi(txt,matubi=4):
    word_counter = Counter()
    for morphemes in make_lines(txt,Flg_matubi=True):
        copus=[d.get('surface') for d in morphemes]
        tmp=""
        end=min([len(copus),matubi])

        for i in reversed(range(1,end+1)):
            tmp+=copus[-i]

        word_counter.update([tmp])                
    return(word_counter)

def count_to_pd(df,df_name,counter,to_csv=False):
    count_word ,count_cnt=zip(*counter.most_common(200))
    s=pd.Series(count_cnt,index=count_word,name=df_name)
    df=pd.concat([df,s],axis=1)
    return(df)