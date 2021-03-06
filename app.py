# The application

# Dependencies
from flask import Flask, session, render_template, request, flash, jsonify, redirect, send_from_directory, url_for
import pandas as pd
import numpy as np
import json

# our modules
from process_input import process_input
from import_lists import import_lists
from now_time import the_time
from predict import PREDICTABO
import report

app = Flask(__name__)

# template file routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def home2():
    return render_template("index.html")

@app.route("/chart.html")
def chart():
    return render_template("chart.html")

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

# the form route!
@app.route('/form.html', methods=['GET', 'POST'])
def form():
    error = ''
    # take in data from form
    
    if request.method == 'POST':
        title = request.form.get('title')
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

        try:
            int(number_of_projects)
        except:
            number_of_projects = 0

        # Now let's make a dictionary to mimic the dataframe from training the model
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
        
        # Put the relevant datetime items into our user input for processing
        del datetimes['now']
        for key, _ in datetimes.items():
            user_input[key] = datetimes[key]
            
        # Now to make it machine learnable, and also one slightly less numerical for our results page
        processed_input, user_data = process_input(user_input, resources_dictionary)
        # And run it through our Geese Howard function to cross counter and get a value
        prediction = PREDICTABO(processed_input)
        
        # Now turn that into a nice %
        pred = round(round(prediction.tolist()[0], 4) *.90 * 100, 2)

        # Generate reports for our output
        essay_report, grade_report, subject_report = report.user_report(user_data)
        return render_template('results.html', pred=pred,
         subject_report=subject_report, essay_report=essay_report, grade_report=grade_report, std_price=user_data['std_price'])
    
    # Otherwise give our form         
    else:
        dropdowns = import_lists()
        # print(dropdowns)
        return render_template('form.html', dropdowns=dropdowns,error=error)


@app.route('/data')
def data():
    df = pd.read_csv('data/census_data.csv')
    return jsonify(df.to_dict(orient="records"))

#this stuff just makes it easier for flask to grab static files

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/stddevthermometer.html')
def thermometer():
    return render_template('stddevthermometer.html')




if __name__ == "__main__":
    app.secret_key = 'my unobvious secret key'
    app.debug = True
    app.run()