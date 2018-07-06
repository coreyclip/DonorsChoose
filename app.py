# The application

# Dependencies
from flask import Flask, render_template, jsonify, redirect, send_from_directory
import pandas as pd

app = Flask(__name__)

# template file routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)



@app.route("/results/<submission>")
def predict(submission):
    prediction = {"results":'none'}
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)