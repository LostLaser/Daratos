import sys
import flask
from flask import request, jsonify
from flask import Flask
from flask import request
import api_exception
import bias_prediction
# import news_scraper

app = flask.Flask(__name__)
app.config["DEBUG"] = True
# scraper = news_scraper.WebDriver(True)

@app.route('/', methods=['GET'])
def info():
    return "Welcome to the political bias API! Go to /bias if you are wanting to get a rating!"

@app.route('/health', methods=['GET'])
def home():
    return "We are up!"

@app.route('/bias', methods=['POST'])
def bias_calc():
    '''
    Endpoint to determine the bias of the specified news article

    Returns:
        Json object of the bias details
    '''
    if not request.json:
        raise api_exception.InvalidUsage('No content specified', status_code = 204)

    json_data = request.get_json()
    content = str(json_data.get('content'))
    verbose = str(json_data.get('verbose'))
    
    if not content or len(content) == 0:
        raise api_exception.InvalidUsage('No content specified', status_code = 204)

    try:
        predictions, sentences = bias_prediction.predict_article(content)
    except EnvironmentError:
        raise api_exception.InvalidUsage('Missing prediction resources', status_code = 503)

    total_bias = bias_prediction.consolidate_biases(predictions)
    if verbose and verbose.lower() == 'true':
        prediction_info = []
        for i in range( min(len(sentences), len(predictions)) ):
            prediction_info.append( { 'sentence': sentences[i],
                                      'prediction': predictions[i]})

        ret_val = {'total_bias': total_bias,
                   'prediction_info': prediction_info}
    else:
        ret_val = {'total_bias': total_bias}
    
    return jsonify(ret_val)

@app.route('/bias/article/xpath')
def retrieve_xpath():
    domain = request.form.get('domain', type = str)

    ret_val = {'domain_xpath': '//div/p'}
    return jsonify(ret_val)

@app.route('/tokenize', methods=['GET'])
def tokenize_sentences():
    content = request.form.get('content', type = str)
    
    sentence_fragments = bias_prediction.tokenize_sentences(content)
    output_tokens = []

    for sentence in sentence_fragments:
        output_tokens.append(sentence[0].tolist())

    ret_val = {'tokenized_sentences': output_tokens}

    return jsonify(ret_val)

@app.errorhandler(api_exception.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

app.run(use_reloader=False)
