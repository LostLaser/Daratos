import flask
from flask import request, jsonify
from flask import Flask
from flask import request
from keras.models import load_model
import numpy
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
        Json object of the bias details
    '''
    ret_val = {}
    content = request.args.get('content',type = str)

    if len(content) == 0:
        return jsonify(ret_val) 
    if model is None or full_processor is None:
        raise API_Exceptions.InvalidUsage('Missing prediction resources', status_code=404)
    
    #Tokenizing the sentences that are inside of input content
    content_sentences = full_processor.split_sentences(content)
    tokenized_sentences = list(map(full_processor.full_clean, content_sentences))

    #Making predictions on each of the sentences
    predictions = []
    with graph.as_default():
        for i in range(len(tokenized_sentences)):
            predictions.extend(model.predict(tokenized_sentences[i]).tolist())

    total_bias = 0.85
    ret_val = {'total_bias': total_bias,
            'sentence_predictions': predictions}
    
    return jsonify(ret_val)

@app.errorhandler(API_Exceptions.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(use_reloader=False)
