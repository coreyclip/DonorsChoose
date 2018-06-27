# The application

# Dependencies
from flask import Flask, render_template, jsonify, redirect
import pandas as pd

app = Flask(__name__)

# template file routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/results/<submission>")
def predict(submission):
    prediction = {"results":'none'}
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)