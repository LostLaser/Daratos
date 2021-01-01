from handlers import api_exception, db_handler, text
from urllib.parse import urlparse
import requests as rqst

import config

MIN_LEFT = -45
FAR_LEFT = -15
LEFT = -5
RIGHT = 5
FAR_RIGHT = 15
MAX_RIGHT = 45

def predict_website(raw_html, url):
    content = text.extract(raw_html)

    if not content or len(content) == 0:
        raise api_exception.InvalidUsage('No content specified', status_code = 204)
    
    parsed_url = urlparse(url)
    url = parsed_url.netloc + parsed_url.path

    # Retrieve prediction value
    if db_handler.is_bias_stored(url, content):
        bias_value = db_handler.get_stored_bias(url, content)
    else:
        total_bias, bias_value = predict(content)
        db_handler.store_bias(url, content, bias_value)
        
    ret_val = {
        'total_bias': total_bias,
        'bias_value': bias_value
    }

    return ret_val

def predict(content):
    data = {
        "Text": str(content),
        "API": str(config.PREDICTION_API_KEY) 
    }
    
    # Send text to bias predictor API
    ret_val = rqst.post(config.PREDICTION_API_URL, data)
    
    if ret_val.status_code not in range(200, 300):
        raise api_exception.InvalidUsage('Error connecting to bias predictor', status_code = 503)
    elif ret_val.text == "Error":
        raise api_exception.InvalidUsage('There was a problem with the api call bias predictor', status_code=400)

    try:
        bias_prediction = float(ret_val.text)
    except:
        raise api_exception.InvalidUsage('Something went wrong', status_code = 400)

    # Putting bias return value into a category
    prediction_category = ""
    
    if FAR_RIGHT <= bias_prediction <= MAX_RIGHT:
        prediction_category = "right"
    elif RIGHT <= bias_prediction <=  FAR_RIGHT:
        prediction_category = "moderately right"
    elif LEFT <= bias_prediction <= RIGHT:
        prediction_category = "neutral"
    elif FAR_LEFT <= bias_prediction <= LEFT:
        prediction_category = "moderately left"
    elif MIN_LEFT <= bias_prediction <=  FAR_LEFT:
        prediction_category = "left"

    return prediction_category, bias_prediction

# check if prediction connection is healthy
def health():
    ret_val = rqst.get(config.PREDICTION_API_URL)

    if ret_val.status_code in range(200, 300):
        return "UP"
    else:
        print(ret_val)
        return "DOWN"