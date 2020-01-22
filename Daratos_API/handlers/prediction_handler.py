import requests as rqst
import config
from handlers import api_exception

MIN_LEFT = -45
FAR_LEFT = -15
LEFT = -5
RIGHT = 5
FAR_RIGHT = 15
MAX_RIGHT = 45

def predict_bias(content):
    data = {
        "Text": str(content),
        "API": str(config.PREDICTION_API_KEY) 
    }
    
    # Send text to bias predictor API
    ret_val = rqst.post(config.PREDICTION_API_URL+"/bert", data)
    
    if ret_val.text == "Error":
        raise api_exception.InvalidUsage('Error connecting to bias predictor', status_code = 400)
    
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