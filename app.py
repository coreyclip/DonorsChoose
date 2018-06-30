# The application

# Dependencies
from flask import Flask, session, render_template, request, flash, jsonify, redirect, send_from_directory, url_for
import pandas as pd
import lightgbm as lgb
import numpy as np
import pickle
import requests

# our modules
import processInput
from import_lists import import_lists

app = Flask(__name__)

# template file routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def home2():
    return render_template("index.html")

@app.route('/form.html', methods=['GET', 'POST'])
def form():
    error = ''
    # take in data from form
    if request.method == 'POST':
        #name = request.form.get('name')
        #email = request.form.get('email')
        school = request.form.get('school')
        city = request.form.get('city')
        state = request.form.get('state')
        essay = request.form.get('essay')
        price = request.form.get('price')
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        about_school = request.form.get('about_school')
        user_input = {
            #'name':name,
            #'email':email, 
            'school':school,
            'about_school':about_school,
            'city':city,
            'state':state,
            'price':price,
            'topic':topic,
            'essay':essay,
            'subject':subject,
            }
        print(user_input)
        #processed_input = processInput.processInput(user_input)
        #print(processed_input)
    else:
        dropdowns = import_lists()
        print(dropdowns)
        return render_template('form.html', dropdowns=dropdowns)

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

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
    app.secret_key = 'my unobvious secret key'
    app.debug = True
    app.run()