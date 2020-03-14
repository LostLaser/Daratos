import requests as rqst
import config
from handlers import api_exception

MIN_LEFT = -45
FAR_LEFT = -15
LEFT = -5
RIGHT = 5
FAR_RIGHT = 15
MAX_RIGHT = 45

def handle(content):
    if not content or len(content) == 0:
        raise api_exception.InvalidUsage('No content specified', status_code = 204)
    
    # Retrieve prediction value
    total_bias, bias_value = predict(content)
    if not total_bias:
        raise api_exception.InvalidUsage('Something went wrong', status_code = 400)
        
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
    ret_val = rqst.post(config.PREDICTION_API_URL+"/bert", data)
    
    if ret_val.status_code not in range(200, 300):
        raise api_exception.InvalidUsage('Error connecting to bias predictor', status_code = 503)
    elif ret_val.text == "Error":
        raise api_exception.InvalidUsage('There was a problem with the api call bias predictor', status_code=400)

    try:
        bias_prediction = float(ret_val.text)
    except:
        return None

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
        return "DOWN"