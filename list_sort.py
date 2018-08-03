# This script creates the dropdown menu file so it will appear alphabetically and without duplicates

# Dependencies
import pandas as pd
import numpy as np
import pickle
import os

# Declare a variable or two we'll use later on to hold things
dicto = {}
cols = ['project_grade_category', 'project_subject_categories', 'project_subject_subcategories', 'school_state', 'teacher_prefix']
dtype = {
    'id': str,
    'teacher_id': str,
    'teacher_prefix': str,
    'school_state': str,
    'project_submitted_datetime': str,
    'project_grade_category': str,
    'project_subject_categories': str,
    'project_title': str,
    'project_subject_subcategories': str,
    'project_essay_1': str,
    'project_essay_2': str,
    'project_essay_3': str,
    'project_essay_4': str,
    'project_resource_summary': str,
    'teacher_number_of_previously_posted_projects': int,
    'project_is_approved': np.uint8,
}
data_path = "D:/DA/uci course stuff/Projects/3/data/"

# Load in the csv file
train = pd.read_csv(os.path.join(data_path, 'train.csv'), dtype=dtype, low_memory=True)

# Process our columns
dicto[cols[0]] = list(train[cols[0]].unique())
dicto[cols[1]] = list(train[train[cols[1]].str.contains(',')==False][cols[1]].sort_values().unique())
dicto[cols[2]] = list(train[train[cols[2]].str.contains(',')==False][cols[2]].sort_values().unique())
dicto[cols[3]] = list(train[cols[3]].sort_values().unique())
dicto[cols[4]] = list(train[train[cols[4]].str.contains('nan')==False][cols[4]].sort_values().unique())

# Save the file
with open('dropdownpop.pk', 'wb') as f:
    pickle.dump(dicto, f)