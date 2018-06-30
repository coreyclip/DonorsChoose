import gc
import numpy as np
import pandas as pd
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, RepeatedKFold
from sklearn.preprocessing import LabelEncoder

from tqdm import tqdm
import lightgbm as lgb

# Load Data
donorsJson = np.load('test_dict.npy').item()

def processInput(donorsDictionary):
    data_path = os.path.join('',)

    # Load the dictionary that you want to test: 
    test = pd.DataFrame.from_dict(donorsDictionary, dtype=str)
    test['teacher_number_of_previously_posted_projects'] = test['teacher_number_of_previously_posted_projects'].astype(int)

    # print(test.shape)

    # res = pd.read_csv(os.path.join(data_path, 'resources.csv'))

    # Preprocess data
    test['project_essay'] = test.apply(lambda row: ' '.join([
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

    extract_features(test)

    test.drop([
        'project_essay_1', 
        'project_essay_2', 
        'project_essay_3', 
        'project_essay_4',
        'teacher_id'], axis=1, inplace=True)

    # df_all = test
    gc.collect()

    # res = pd.DataFrame(res[['id', 'quantity', 'price']].groupby('id').agg(\
    #     {
    #         'quantity': [
    #             'sum',
    #             'min', 
    #             'max', 
    #             'mean', 
    #             'std', 
    #             # lambda x: len(np.unique(x)),
    #         ],
    #         'price': [
    #             'count', 
    #             'sum', 
    #             'min',
    #             'max', 
    #             'mean', 
    #             'std', 
    #             lambda x: len(np.unique(x)),
    #         ]}
    #     )).reset_index()
    # res.columns = ['_'.join(col) for col in res.columns]
    # res.rename(columns={'id_': 'id'}, inplace=True)
    # res['mean_price'] = res['price_sum']/res['quantity_sum']

    # print(res.head())
    # test = test.merge(res, on='id', how='left')
    # del res
    # gc.collect()

    # Preprocess columns with label encoder
    # print('Label Encoder...')
    cols = [
        'teacher_prefix', 
        'school_state', 
        'project_grade_category', 
        'project_subject_categories', 
        'project_subject_subcategories'
    ]

    for c in cols:
        filename = c + '_encoder.pk'
        with open(filename, 'rb') as f:
            le = pickle.load(f)
        d = c + '_encoded'
        test[d] = le.transform(test[c].astype(str))
        test.drop([c], axis=1, inplace=True)
    del le
    gc.collect()
    # print('Done.')


    # Preprocess timestamp
    # print('Preprocessing timestamp...')
    # def process_timestamp(df):
    #     df['year'] = df['project_submitted_datetime'].apply(lambda x: int(x.split('-')[0]))
    #     df['month'] = df['project_submitted_datetime'].apply(lambda x: int(x.split('-')[1]))
    #     df['date'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[0].split('-')[2]))
    #     df['day_of_week'] = pd.to_datetime(df['project_submitted_datetime']).dt.weekday
    #     df['hour'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[-1].split(':')[0]))
    #     df['minute'] = df['project_submitted_datetime'].apply(lambda x: int(x.split(' ')[-1].split(':')[1]))
    #     df['project_submitted_datetime'] = pd.to_datetime(df['project_submitted_datetime']).values.astype(np.int64)

    # process_timestamp(test)
    # print('Done.')

    # Preprocess text
    # print('Preprocessing text...')
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
    
    for c in cols:
        d = 0
        filename = c + '_tfidf.pk'
        with open(filename, 'rb') as f:
            tfidf = pickle.load(f)
    
        tfidf_test = np.array(tfidf.transform(test[c]).toarray(), dtype=np.float16)
        for i in range(n_features[d]):
                test[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
        
        d += 1
        del tfidf, tfidf_test
        gc.collect()
        # print('project_title_tfidf Done.')

    # Prepare data
    cols_to_drop = [
        'id',
        'teacher_id',
        'project_title', 
        'project_essay', 
        'project_resource_summary',
        'project_is_approved',
    ]
    X_test = test.drop(cols_to_drop, axis=1, errors='ignore')
    # id_test = test['id'].values

    del test
    gc.collect()

    # load model to predict

    with open('model_v1.pkl', 'rb') as f:
        model = pickle.load(f)

    #predict
    results = model.predict(X_test)
    return results[0]