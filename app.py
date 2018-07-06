# The application

# Dependencies
from flask import Flask, session, render_template, request, flash, jsonify, redirect, send_from_directory, url_for
import pandas as pd
import numpy as np

# our modules
from process_input import process_input
from import_lists import import_lists
from now_time import the_time
from predict import PREDICTABO

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
        title = request.form.get('title')
        #email = request.form.get('email')
        prefix = request.form.get('prefix')
        state = request.form.get('state')
        datetimes = the_time()
        grade = request.form.get('grade')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        number_of_projects = request.form.get('projects')
        essay_1 = request.form.get('essay1')
        essay_2 = request.form.get('essay2')
        essay_3 = ''
        essay_4 = ''
        resources = ''
        resources_dictionary = {
            'price': request.form.get('price'),
            'quantity': request.form.get('quantity')
        }

        user_input = {
            'project_title': title,
            'teacher_prefix': prefix,
            'school_state': state,
            'project_submitted_datetime': datetimes['now'],
            'project_grade_category': grade,
            'project_subject_categories': category,
            'project_subject_subcategories': subcategory,
            'teacher_number_of_previously_posted_projects': number_of_projects,
            'project_essay_1': essay_1,
            'project_essay_2': essay_2,
            'project_essay_3': essay_3,
            'project_essay_4': essay_4,
            'project_resource_summary': resources
            }
        del datetimes['now']
        for key, _ in datetimes.items():
            user_input[key] = datetimes[key]
        print(user_input)
        processed_input = process_input(user_input, resources_dictionary)
        # print(processed_input)
        prediction = PREDICTABO(processed_input)
        # return render_template('results.html')
        print(prediction)
        return jsonify(prediction.tolist())
    else:
        dropdowns = import_lists()
        # print(dropdowns)
        return render_template('form.html', dropdowns=dropdowns,error=error)

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

@app.route("/results/<submission>", methods=['GET'])
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