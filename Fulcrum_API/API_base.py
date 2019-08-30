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
import API_Exceptions

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Loading items needed for prediction
try:
    full_processor = TextProcessor.ProcessRaw()
except OSError:
    full_processor = None
try:
    model = load_model('sentenceModel.h5')
    model._make_predict_function()
except IOError:
    model = None
graph = tf.get_default_graph()

@app.route('/', methods=['GET'])
def info():
    return "Welcome to the political bias API! Go to /bias if you are wanting to get a rating!"

@app.route('/health', methods=['GET'])
def home():
    return "<p>We are up!</p>"

@app.route('/bias', methods=['GET'])
def bias_calc():
    '''
    Endpoint to determine the bias of the specified news article

    Returns:
        Json object of the total bias
    '''
    ret_val = {}
    if model is not None and full_processor is not None:
        content = request.args.get('content',type = str)
        content_train = full_processor.full_clean(content)
        if len(content_train) == 0:
            return jsonify({'lean': "Nothing selected"}) 
        with graph.as_default():
            outputs = model.predict(content_train)
        for i in range(len(outputs)):
            print("Left chance=" + str(outputs[i][0]) + "; Neutral chance=" + str(outputs[i][1]) + "; Right chance=" + str(outputs[i][2]))

        lean_val = "Left chance=" + str(outputs[0][0]) + " Neutral chance=" + str(outputs[0][1]) + " Right chance=" + str(outputs[0][2])
        confidence_val = 0.85
        ret_val = {'lean': lean_val,
                'confidence': confidence_val}
    else:
        raise API_Exceptions.InvalidUsage('Missing prediction resources', status_code=404)
    
    return jsonify(ret_val)

@app.errorhandler(API_Exceptions.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(use_reloader=False)
