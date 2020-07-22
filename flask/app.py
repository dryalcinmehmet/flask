#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:52:58 2020

@author: myalcin
"""

import sys
import os
import shutil
import time
import traceback
import psycopg2

import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_score, accuracy_score, recall_score

from flask import Flask, request, jsonify
import pandas as pd
import json
from sklearn.externals import joblib

app = Flask(__name__)



class SVM:
    def __init__(self,*args,**kwargs):
        pass
        
    def create_data(self,file):
      
        import psycopg2 as pg
        import pandas.io.sql as psql
        connection = pg.connect("host=localhost dbname=cognitus2 user=testuser password=test")
        dataframe = psql.read_sql('SELECT * FROM dataset', connection)
        
            
        return dataframe['text'].tolist(), dataframe['label'].tolist()
        


    #feature extraction - creating a tf-idf matrix
    def tfidf(self,data, ma = 0.6, mi = 0.0001):
        tfidf_vectorize = TfidfVectorizer()
        tfidf_data = tfidf_vectorize.fit_transform(data)
        return tfidf_data, tfidf_vectorize
    
    
    #SVM classifier
    def test_SVM(self,x_train, x_test, y_train, y_test):
        SVM = SVC(kernel = 'linear')
        SVMClassifier = SVM.fit(x_train, y_train)
        predictions = SVMClassifier.predict(x_test)
        a = accuracy_score(y_test, predictions)
        p = precision_score(y_test, predictions, average = 'weighted')
        r = recall_score(y_test, predictions, average = 'weighted')
        return SVMClassifier, a, p, r
    
    
    
    def dump_model(self,model, file_output):
        pickle.dump(model, open(file_output, 'wb'))
    
    def load_model(self,file_input):
        return pickle.load(open(file_input, 'rb'))

@app.route('/predict', methods=['POST']) # Create http://host:port/predict POST end point
def predict():
    
    svmOBJ = SVM()
    # need posted data here
    try:
        # PREDICTION
        
        user_text = request.args.get('user_text')
        model = svmOBJ.load_model('/home/swisyn/Desktop/Cognitus_task/model.pickle')
        vectorizer = svmOBJ.load_model('/home/swisyn/Desktop/Cognitus_task/vectorizer.pickle')
        result = model.predict(vectorizer.transform([user_text]))
        print(type(result))
        
        return jsonify({'prediction': str(result[0])})
        
        
    except Exception as e:

        return jsonify({'error': str(e), 'trace': traceback.format_exc()})


@app.route('/train', methods=['GET']) # Create http://host:port/train GET end point
def train():
    svmOBJ = SVM()
    
    # GET DATA
    file = "/home/swisyn/Desktop/Cognitus_task/test_data.xlsx"
    text, label = svmOBJ.create_data(file)

    # TRAIN
    training, vectorizer = svmOBJ.tfidf(text)
    x_train, x_test, y_train, y_test = train_test_split(training, label, test_size = 0.25, random_state = 0)
    model, accuracy, precision, recall = svmOBJ.test_SVM(x_train, x_test, y_train, y_test)
    svmOBJ.dump_model(model, 'model.pickle')
    svmOBJ.dump_model(vectorizer, 'vectorizer.pickle')


    return 'Success'


@app.route('/wipe', methods=['GET']) # Create http://host:port/wipe GET end point
def wipe():
    try:
        shutil.rmtree('model')
        os.makedirs(model_directory)
        return 'Model wiped'

    except Exception as e:
        print(str(e))
        return 'Could not remove and recreate the model directory'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 80

    try:
        clf = joblib.load(model_file_name)
        print('model loaded')
        model_columns = joblib.load(model_columns_file_name)
        print('model columns loaded')

    except Exception as e:
        print('No model here')
        print('Train first')
        print(str(e))
        clf = None

    app.run(host='0.0.0.0', port=8080,debug=True)

