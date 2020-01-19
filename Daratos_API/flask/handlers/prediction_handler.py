import requests as rqst
import config
from handlers import api_exception

FAR_LEFT = 7
LEFT = 1
RIGHT = -1
FAR_RIGHT = -7

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

    print(bias_prediction)
    # Putting bias return value into a category
    prediction_category = ""
    
    if bias_prediction < FAR_RIGHT :
        prediction_category = "right"
    elif FAR_RIGHT <= bias_prediction <= RIGHT:
        prediction_category = "moderately right"
    elif RIGHT <= bias_prediction <= LEFT:
        prediction_category = "neutral"
    elif bias_prediction > FAR_LEFT:
        prediction_category = "left"
    elif FAR_LEFT >= bias_prediction >= LEFT:
        prediction_category = "moderately left"
    
    return prediction_category