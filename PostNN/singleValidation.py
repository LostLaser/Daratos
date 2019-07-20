#!flask/bin/python
from flask import Flask
from flask import request
from numpy import loadtxt
from keras.models import load_model
import numpy
from keras.preprocessing import sequence as sqc
from keras.preprocessing.text import Tokenizer
import pickle
import keras
import tensorflow as tf
import sys
import clean_string
import nltk

model = load_model('Models/my_model.h5')
model._make_predict_function()
global graph
graph = tf.get_default_graph()
with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

stop_words = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.PorterStemmer()

content=""
content=clean_string.clean(content, stemmer, stop_words)
encoded_content_train = tokenizer.texts_to_sequences([content])
encoded_content_train = sqc.pad_sequences(encoded_content_train, maxlen=1000)
content_train = numpy.array(encoded_content_train)

with graph.as_default():
    outputs = model.predict(content_train)
print(outputs)
print("Hello, World! and "+str(outputs[0][0]))