import numpy as np
import pandas as pd
import os
import pickle

with open('model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

def process_input(data):
    # Load the dictionary that you want to test: 
    data['project_essay'] = ' '.join([data['project_essay_1'], data['project_essay_2'], data['project_essay_3'], data['project_essay_4']])

    # Extract features
    # lengths
    data['project_title_len'] = len(data['project_title'])
    data['project_essay_1_len'] = len(data['project_essay_1'])
    data['project_essay_2_len'] = len(data['project_essay_2'])
    data['project_essay_3_len'] = len(data['project_essay_3'])
    data['project_essay_4_len'] = len(data['project_essay_4'])
    
    # word counts
    data['project_title_wc'] = len(data['project_title'].split(' '))
    data['project_essay_1_wc'] = len(data['project_essay_1'].split(' '))
    data['project_essay_2_wc'] = len(data['project_essay_2'].split(' '))
    data['project_essay_3_wc'] = len(data['project_essay_3'].split(' '))
    data['project_essay_4_wc'] = len(data['project_essay_4'].split(' '))
    
    # these will be implemented later
    data['project_resource_summary_len'] = 0
    data['project_resource_summary_wc'] = 0

    data.to_csv('../static/data/user.csv')

    # encode our categorical data as numbers
    keys = ['teacher_prefix', 'school_state', 'project_grade_category', 'project_subject_categories', 'project_subject_subcategories']
    for key in keys:
        filename = key + '_encoder.pk'
        with open(filename, 'rb') as f:
            le = pickle.load(f)
        d = key + '_encoded'
        data[d] = le.transform([data[key]])
        del data[key]
    del le

    # TfIdf vectors
    keys = ['project_title', 'project_essay', 'project_resource_summary']
    n_features = [400, 4040, 400,]
    for key in keys:
        d = 0
        filename = key + '_tfidf.pk'
        with open(filename, 'rb') as f:
            tfidf = pickle.load(f)
    
        tfidf_test = np.array(tfidf.transform([data[key]]).toarray(), dtype=np.float16)
        for i in range(n_features[d]):
                data[key + '_tfidf_' + str(i)] = tfidf_test[:, i]
        
        d += 1
        del tfidf, tfidf_test

   # get rid of some keys we don't need anymore
    keys = ['project_title', 'project_essay', 'project_resource_summary', 'project_essay_1', 'project_essay_2', 'project_essay_3', 'project_essay_4', 'teacher_id']
    for key in keys:
        if key in data:
            del data[key]

    return data
