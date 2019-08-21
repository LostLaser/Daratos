import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def info():
    return "Welcome to the political bias API! Go to /bias if you are wanting to get a rating!"

@app.route('/health', methods=['GET'])
def home():
    return "<p>We are up!</p>"

@app.route('/bias', methods=['GET'])
def bias_calc():
    lean_val = 'left'
    confidence_val = 0.85
    ret_val = {'lean': lean_val,
               'confidence': confidence_val}
    
    return jsonify(ret_val)

app.run()
