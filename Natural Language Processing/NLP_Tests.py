# -*- coding: "ISO-8859-1 -*-
"""
Created on Wed Apr  9 11:34:23 2021

@author: mjvat
"""
import pandas as pd
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

def clean_text(text, stopwords):
    
    words = text.split()
    cleaned_text = []
    
    for word in words:
        if word.lower() not in stopwords:
            cleaned_text.append(word)
    corpus = ' '.join(cleaned_text)
    return corpus

def getData(name):
    
    dataset = pd.read_csv(name, encoding='ISO-8859-1', header=0)
    data_x = dataset['text']

    if name=="imdb_tr.csv":
        data_y = dataset['polarity']
        return data_x, data_y

    return data_x

def imdb_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):

    count = 0
    counter = []
    text = []
    reviews = []
    
    stopwords = open("stopwords.en.txt", 'r', encoding="ISO-8859-1").read().split('\n')
    
    for path in os.listdir(inpath + "pos"):
        inputs = open(inpath + "pos/" + path, 'r', encoding="ISO-8859-1").read()
        inputs = clean_text(inputs, stopwords)
        counter.append(count)
        text.append(inputs)
        reviews.append("1")
        
    for path in os.listdir(inpath + "neg"):
        inputs = open(inpath + "neg/" + path, 'r', encoding="ISO-8859-1").read()
        inputs = clean_text(inputs, stopwords)
        counter.append(count)
        text.append(inputs)
        reviews.append("0")
    
    results = list(zip(counter, text, reviews))

    if mix:
        np.random.shuffle(results)

    data = pd.DataFrame(data=results, columns=['row_Number', 'text', 'polarity'])
    data.to_csv(outpath + name, index=False, header=True)

def outputFile(results, filename):
    results = '\n'.join(str(result) for result in results)
    file = open(filename,'w')
    file.write(results)
    file.close()

def unigram(data):
    cv = CountVectorizer()
    cv = cv.fit(data)
    return cv

def stochasticDescent(train_x, train_y, test_x):
    classifier = SGDClassifier(loss='hinge', penalty='l1')
    classifier.fit(train_x, train_y)
    preds = classifier.predict(test_x)
    return preds

def tfidf(data):
    tcv = TfidfTransformer()
    tcv = tcv.fit(data)
    return tcv
    
if __name__ == "__main__":
    
    train_path = "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
    test_path = "../resource/lib/publicdata/imdb_te.csv"  # test data for grade evaluation

    imdb_preprocess(inpath=train_path, mix=True)    
    train_x, train_y = getData(name="imdb_tr.csv")
    test_x = getData(name=test_path)

    # Unigram
    uni_vec = unigram(train_x)
    uni_train_x = uni_vec.transform(train_x)
    
    uni_test_x = uni_vec.transform(test_x)
    uni_test_y = stochasticDescent(uni_train_x, train_y, uni_test_x)
    outputFile(uni_test_y, 'unigram.output.txt')

    # Unigram-TFidf
    uni_tf_trans = tfidf(uni_train_x)
    uni_tf_train_x = uni_tf_trans.transform(uni_train_x)
    uni_tf_test_x = uni_tf_trans.transform(uni_test_x)
    uni_tf_test_y = stochasticDescent(uni_tf_train_x, train_y, uni_tf_test_x)
    outputFile(uni_tf_test_y, 'unigramtfidf.output.txt')
