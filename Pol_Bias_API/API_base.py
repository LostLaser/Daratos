import flask
from flask import request, jsonify
from flask import Flask
from flask import request
from numpy import loadtxt
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import keras
import tensorflow as tf
import sys
import TextProcessor

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Loading items needed for prediction
full_processor = TextProcessor.ProcessRaw()
graph = tf.get_default_graph()
model = load_model('sentenceModel.h5')
model._make_predict_function()

@app.route('/', methods=['GET'])
def info():
    return "Welcome to the political bias API! Go to /bias if you are wanting to get a rating!"

@app.route('/health', methods=['GET'])
def home():
    return "<p>We are up!</p>"

@app.route('/bias', methods=['GET'])
def bias_calc():
    content=request.args.get('content',type = str)
    content_train = full_processor.full_clean(content)
    if len(content_train) == 0:
        return jsonify({'lean': "Nothing selected"}) 
    with graph.as_default():
        outputs = model.predict(content_train)
    print(outputs)
    for i in range(len(outputs)):
        print("Left chance=" + str(outputs[i][0]) + "; Neutral chance=" + str(outputs[i][1]) + "; Right chance=" + str(outputs[i][2]))

    lean_val = "Left chance=" + str(outputs[0][0]) + " Neutral chance=" + str(outputs[0][1]) + " Right chance=" + str(outputs[0][2])
    confidence_val = 0.85
    ret_val = {'lean': lean_val,
               'confidence': confidence_val}
    
    return jsonify(ret_val)

app.run(use_reloader=False)
