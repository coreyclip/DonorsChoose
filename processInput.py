import numpy as np
import pandas as pd
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, RepeatedKFold
from sklearn.preprocessing import LabelEncoder

import lightgbm as lgb

# Load test Data
# donorsJson = np.load('test_dict.npy').item()

# Define the function: 
def processInput(donorsDictionary):
    
    #container to hold vocabs
    vocabs = {}

    #container to hold inverse transforms
    inverse_transforms = {}

    data_path = os.path.join('',)

    # Load the dictionary that you want to test: 
    input_dict = donorsDictionary
    user_input = pd.DataFrame.from_dict(input_dict, dtype=str)
    user_input['teacher_number_of_previously_posted_projects'] = user_input['teacher_number_of_previously_posted_projects'].astype(int)

    print('shape of user input: ', user_input.shape)
    
    # load resources
    res = pd.read_csv(os.path.join(data_path, 'resources.csv'))

    # Preprocess data
    user_input['project_essay'] = user_input.apply(lambda row: ' '.join([
        str(row['project_essay_1']),
        str(row['project_essay_2']), 
        str(row['project_essay_3']), 
        str(row['project_essay_4']),
        ]), axis=1)

    # Extract features
    def extract_features(df):
        df['project_title_len'] = df['project_title'].apply(lambda x: len(str(x)))
        df['project_essay_1_len'] = df['project_essay_1'].apply(lambda x: len(str(x)))
        df['project_essay_2_len'] = df['project_essay_2'].apply(lambda x: len(str(x)))
        df['project_essay_3_len'] = df['project_essay_3'].apply(lambda x: len(str(x)))
        df['project_essay_4_len'] = df['project_essay_4'].apply(lambda x: len(str(x)))
        df['project_resource_summary_len'] = df['project_resource_summary'].apply(lambda x: len(str(x)))

        df['project_title_wc'] = df['project_title'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_1_wc'] = df['project_essay_1'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_2_wc'] = df['project_essay_2'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_3_wc'] = df['project_essay_3'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_4_wc'] = df['project_essay_4'].apply(lambda x: len(str(x).split(' ')))
        df['project_resource_summary_wc'] = df['project_resource_summary'].apply(lambda x: len(str(x).split(' ')))

    extract_features(user_input)

    user_input.drop([
        'project_essay_1', 
        'project_essay_2', 
        'project_essay_3', 
        'project_essay_4'], axis=1, inplace=True)

    df_all = user_input

    # init results
    res = pd.DataFrame(res[['id', 'quantity', 'price']].groupby('id').agg(\
        {
            'quantity': [
                'sum',
                'min', 
                'max', 
                'mean', 
                'std', 
                # lambda x: len(np.unique(x)),
            ],
            'price': [
                'count', 
                'sum', 
                'min',
                'max', 
                'mean', 
                'std', 
                lambda x: len(np.unique(x)),
            ]}
        )).reset_index()
    res.columns = ['_'.join(col) for col in res.columns]
    res.rename(columns={'id_': 'id'}, inplace=True)
    res['mean_price'] = res['price_sum']/res['quantity_sum']

    print('results column: ', res.head())
    user_input = user_input.merge(res, on='id', how='left')
    del res

    # Preprocess columns with label encoder
    print('Label Encoder...')
    cols = [
        'teacher_id', 
        'teacher_prefix', 
        'school_state', 
        'project_grade_category',
        'project_subject_categories', 
        'project_subject_subcategories'
    ]
    inverse_transform = {}
    for c in cols:
        le = LabelEncoder()
        le.fit(df_all[c].astype(str))
        user_input[c] = le.transform(user_input[c].astype(str))
        inverse_transform[c] = {le.inverse_transform(user_input[c]), user_input[c]}
    
    print('Done. user input:\n', user_input)

    inverse_transforms['project_title'] = inverse_transform

    # Preprocess timestamp
    print('Preprocessing timestamp...')
    def process_timestamp(df):
        df['year'] = df['project_submitted_datetime'].apply(lambda x: int(x.split('-')[0]))
        df['month'] = df['project_submitted_datetime'].apply(lambda x: int(x.split('-')[1]))
        df['date'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[0].split('-')[2]))
        df['day_of_week'] = pd.to_datetime(df['project_submitted_datetime']).dt.weekday
        df['hour'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[-1].split(':')[0]))
        df['minute'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[-1].split(':')[1]))
        df['project_submitted_datetime'] = pd.to_datetime(df['project_submitted_datetime']).values.astype(np.int64)

    process_timestamp(user_input)
    print('Done.')

    # Preprocess text
    print('Preprocessing text...')
    cols = [
        'project_title', 
        'project_essay', 
        'project_resource_summary'
    ]
    n_features = [
        400, 
        4040, 
        400,
    ]

    with open('project_title_tfidf.pk', 'rb') as f:
        project_title_tfidf = pickle.load(f)

#     tfidf = TfidfVectorizer(
#         max_features=n_features[0],
#         norm='l2',
#         )
    print('project title tfidf vocab:\n', project_title_tfidf.vocabulary_)
    
    vocabs['project_title_vocab'] = project_title_tfidf.vocabulary_
    
    tfidf_test = np.array(project_title_tfidf.transform(user_input['project_title']).toarray(), dtype=np.float16)
    
    for i in range(n_features[0]):
            user_input[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
    del project_title_tfidf, tfidf_test
    gc.collect()
    print('project_title_tfidf Done.')

    with open('project_essay_tfidf.pk', 'rb') as f:
        project_essay_tfidf = pickle.load(f)
    
    vocabs['project_essay_tfidf'] = project_essay_tfidf.vocabulary_
    
#     tfidf = TfidfVectorizer(
#         max_features=n_features[1],
#         norm='l2',
#         )

    tfidf_test = np.array(project_essay_tfidf.transform(user_input['project_resource_summary']).toarray(), dtype=np.float16)

    for i in range(n_features[1]):
            user_input[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
    del project_essay_tfidf, tfidf_test
    gc.collect()
    print('project_essay_tfidf Done.')

    with open('project_resource_summary_tfidf.pk', 'rb') as f:
        project_resource_summary_tfidf = pickle.load(f)

#     tfidf = TfidfVectorizer(
#         max_features=n_features[2],
#         norm='l2',
#         )
    vocabs['project_resource_summary_tfidf'] = project_resource_summary_tfidf.vocabulary_    

    tfidf_test = np.array(project_resource_summary_tfidf.transform(user_input['project_resource_summary']).toarray(), dtype=np.float16)

    for i in range(n_features[2]):
            user_input[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
    del project_resource_summary_tfidf, tfidf_test
    gc.collect()
    print('project_resource_summary_tfidf Done.')

    # Prepare data
    cols_to_drop = [
        'id',
        'teacher_id',
        'project_title', 
        'project_essay',
        'project_resource_summary',
        'project_is_approved',
    ]
    
    X_test = user_input.drop(cols_to_drop, axis=1, errors='ignore')
    id_test = user_input['id'].values

    # Build the model
    cnt = 0
    p_buf = []
    n_splits = 5
    n_repeats = 1

    auc_buf = []   

    # load model to predict

    print('Load model to predict')
    imported_model = pickle.load( open( "model_v1.pkl", "rb" ) )
    print('model loaded')
    #predict
    results = imported_model.predict(X_test)
    features = X_test
    feature_names = X_test.columns.tolist()
    return {results[0], features, feature_names, vocabs, inverse_transform}