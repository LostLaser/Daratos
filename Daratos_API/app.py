import sys
from flask import request, jsonify, Flask

from handlers import db_handler, prediction_handler, api_exception
import config
import requests as rqst

app = Flask(__name__)

@app.route('/')
def info():
    return 'Welcome to the political bias API! Go to /bias if you are wanting to get a prediction!'

@app.route('/health', methods=['GET'])
def home():
    health = {}
    health["Status"] = "UP"
    health["DB"] = db_handler.db_health()
    health["Prediction AI"] = prediction_handler.prediction_health()

    return jsonify(health)

@app.route('/bias', methods=['POST'])
def bias_calc():
    '''
    Endpoint to determine the bias of the specified news article

    Parameters: 
        content (str): String containing sentences

    Returns:
        Json object of the bias details
    '''
    if not request.json:
        raise api_exception.InvalidUsage('Missing json request body', status_code = 400)
    
    json_data = request.get_json()
    content = str(json_data.get('content'))
    
    if not content or len(content) == 0:
        raise api_exception.InvalidUsage('No content specified', status_code = 204)
    
    # Retrieve prediction value
    total_bias, bias_value = prediction_handler.predict_bias(content)
    if not total_bias:
        raise api_exception.InvalidUsage('Something went wrong', status_code = 400)
        
    ret_val = {
        'total_bias': total_bias,
        'bias_value': bias_value      
    }
    
    return jsonify(ret_val)

@app.route('/article/xpath', methods=['POST'])
def retrieve_xpath():
    '''
    Endpoint to determine the web scraping details of a news website

    Parameters: 
        domain (str): domain name of a supported news website

    Returns:
        Json object containing the xpath
    '''
    json_data = request.get_json()
    x_path = ""

    if json_data:
        domain = str(json_data.get('domain'))
        x_path = db_handler.get_xpath(domain)

    ret_val = {'domain_xpath': x_path}
    return jsonify(ret_val)

@app.errorhandler(api_exception.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE, use_reloader=False)