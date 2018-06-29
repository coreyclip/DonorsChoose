# The application

# Dependencies
from flask import Flask, render_template, jsonify, redirect, send_from_directory
import pandas as pd
import lightgbm as lgb
import numpy as np

try:
    import cPickle as pickle
except BaseException:
    import pickle

# our modules
import processInput

with open('model_v1.pkl', 'rb') as fin:
    model = pickle.load(fin)

app = Flask(__name__)

# template file routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/results/<submission>")
def predict(submission):
    #cleaned = clean(submission)
    

    prediction = {"results":'none'}
    return jsonify(prediction)



#this stuff just makes it easier for flask to grab static files

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)




if __name__ == "__main__":
    app.run(debug=True)