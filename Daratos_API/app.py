import sys
from flask import request, jsonify, Flask
from flask_cors import CORS, cross_origin

from handlers import db_handler, bias, api_exception, text
import config

app = Flask(__name__)

@app.route('/')
def info():
    return 'Welcome to the political bias API! Go to /bias if you are wanting to get a prediction!'

@app.route('/health', methods=['GET'])
def home():
    health = {}
    health["Status"] = "UP"
    health["DB"] = db_handler.db_health()
    health["Prediction AI"] = bias.health()

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
    
    prediciton = bias.handle(content)
    
    return jsonify(prediciton)

@app.route('/bias/html', methods=['POST'])
@cross_origin()
def bias_html():
    '''
    Endpoint to predict the bias of a provided news article given raw html

    Parameters: 
        html (str): html of a news article

    Returns:
        Json object containing the bias prediction
    '''
    if not request.json:
        raise api_exception.InvalidUsage('Missing json request body', status_code = 400)
    
    json_data = request.get_json()
    raw_html = str(json_data.get('raw_html'))

    content = text.extract(raw_html)
    
    prediciton = bias.handle(content)

    return jsonify(prediciton)

@app.route('/extract/html', methods=['POST'])
def extract_html():
    '''
    Endpoint to extract the content of a provided news article

    Parameters: 
        html (str): html of a news article

    Returns:
        Json object containing the article content
    '''
    if not request.json:
        raise api_exception.InvalidUsage('Missing json request body', status_code = 400)
    
    json_data = request.get_json()
    if json_data.get('raw_html') is None:
        raise api_exception.InvalidUsage('Missing field <raw_html>', status_code = 400)
    raw_html = str(json_data.get('raw_html'))

    content = text.extract(raw_html)

    return jsonify({"content": content})

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