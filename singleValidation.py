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

model = load_model('Models/my_model.h5')
model._make_predict_function()
global graph
graph = tf.get_default_graph()
with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

content="Thursday’s sham social media summit at the White House might have already disproved its own point by being one of the most posted-about things on social media. The summit, a motley crew of Trump supporters and online trolls — pointedly devoid of anyone from a real social media company — met to discuss their baseless theory that conservative voices have been systematically suppressed on social media. The event was more popular on social media on the day of the summit than 7-Eleven Day, a promoted and highly discussed annual occurrence in which the convenience store chain gives away free Slurpees, according to data from social media measurement companies Hootsuite and Crimson Hexagon. It was also more popular than tweets about the Women’s World Cup winners, who had celebrated their victory parade in New York just the day before. Both companies performed a variety of keyword searches to try and include the many ways in which people were talking about these subjects. Crimson Hexagon found that nearly 170,000 tweets and retweets were about the social media summit, compared to 90,000 for 7-Eleven and just over 100,000 for the Women’s World Cup. On the day of the US women’s soccer team victory, however, that topic owned, with nearly 2 million tweets and retweets. Even Trump tweeted about it. Hootsuite, which gathers this info on Twitter, Facebook, Instagram, and Reddit, among others, through its social media monitoring integration with Brandwatch, didn’t provide exact numbers but said the summit had twice as many mentions as #FreeSlurpeeDay and that it surpassed mentions for the Women’s World Cup from the day before. But the summit wasn’t the biggest Twitter topic on Thursday. The top three biggest topics were convicted sex offender Jeffrey Epstein, his friend Donald Trump, and Korean pop band BTS, according to Crimson Hexagon, but the summit was certainly one of the more prominent social media topics in the US on that day. But not all social media is good social media."
encoded_content_train = tokenizer.texts_to_sequences([content])
encoded_content_train = sqc.pad_sequences(encoded_content_train, maxlen=1000)
content_train = numpy.array(encoded_content_train)

with graph.as_default():
    outputs = model.predict(content_train)
print(outputs)
print("Hello, World! and "+str(outputs[0][0]))