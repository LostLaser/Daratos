import flask
from flask import request, jsonify
from flask import Flask
from flask import request
import sys
import api_exceptions
import bias_prediction

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def info():
    return "Welcome to the political bias API! Go to /bias if you are wanting to get a rating!"

@app.route('/health', methods=['GET'])
def home():
    return "We are up!"

@app.route('/bias', methods=['GET'])
def bias_calc():
    '''
    Endpoint to determine the bias of the specified news article

    Returns:
        Json object of the bias details
    '''
    ret_val = {}
    content = request.args.get('content', type = str)
    if len(content) == 0:
        return jsonify(ret_val)

    try:
        predictions, _ = bias_prediction.predict_article(content)
    except EnvironmentError:
        api_exceptions.InvalidUsage('Missing prediction resources', status_code = 404)

    total_bias = bias_prediction.determine_article_bias(predictions)
    ret_val = {'total_bias': total_bias,
            'sentence_predictions': predictions}
    
    return jsonify(ret_val)

@app.errorhandler(api_exceptions.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(use_reloader=False)
