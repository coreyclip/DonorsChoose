import gc
import numpy as np
import pandas as pd
import os

try:
    import cPickle as pickle
except BaseException:
    import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold, RepeatedKFold
from sklearn.preprocessing import LabelEncoder

from tqdm import tqdm
import lightgbm as lgb

# Load Data
dtype = {
    'id': str,
    'teacher_id': str,
    'teacher_prefix': str,
    'school_state': str,
    'project_submitted_datetime': str,
    'project_grade_category': str,
    'project_subject_categories': str,
    'project_subject_subcategories': str,
    'project_title': str,
    'project_essay_1': str,
    'project_essay_2': str,
    'project_essay_3': str,
    'project_essay_4': str,
    'project_resource_summary': str,
    'teacher_number_of_previously_posted_projects': int,
    'project_is_approved': np.uint8,
}
data_path = os.path.join('',)

# Load the dictionary that you want to test: 
test_dict = np.load('test_dict.npy').item()
test = pd.DataFrame.from_dict(test_dict, dtype=str)
test['teacher_number_of_previously_posted_projects'] = test['teacher_number_of_previously_posted_projects'].astype(int)

print(test.shape)

res = pd.read_csv(os.path.join(data_path, 'resources.csv'))

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
    'project_essay_4'], axis=1, inplace=True)

df_all = test
gc.collect()

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

print(res.head())
test = test.merge(res, on='id', how='left')
del res
gc.collect()

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

for c in tqdm(cols):
    le = LabelEncoder()
    le.fit(df_all[c].astype(str))
    test[c] = le.transform(test[c].astype(str))
del le
gc.collect()
print('Done.')


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

process_timestamp(test)
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
    
tfidf = TfidfVectorizer(
    max_features=n_features[0],
    norm='l2',
    )

tfidf_test = np.array(project_title_tfidf.transform(test['project_title']).toarray(), dtype=np.float16)

for i in range(n_features[0]):
        test[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
del project_title_tfidf, tfidf_test
gc.collect()
print('project_title_tfidf Done.')

with open('project_essay_tfidf.pk', 'rb') as f:
    project_essay_tfidf = pickle.load(f)
    
tfidf = TfidfVectorizer(
    max_features=n_features[1],
    norm='l2',
    )

tfidf_test = np.array(project_essay_tfidf.transform(test['project_resource_summary']).toarray(), dtype=np.float16)

for i in range(n_features[1]):
        test[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
del project_essay_tfidf, tfidf_test
gc.collect()
print('project_essay_tfidf Done.')

with open('project_resource_summary_tfidf.pk', 'rb') as f:
    project_resource_summary_tfidf = pickle.load(f)
    
tfidf = TfidfVectorizer(
    max_features=n_features[2],
    norm='l2',
    )

tfidf_test = np.array(project_resource_summary_tfidf.transform(test['project_resource_summary']).toarray(), dtype=np.float16)

for i in range(n_features[2]):
        test[c + '_tfidf_' + str(i)] = tfidf_test[:, i]
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
X_test = test.drop(cols_to_drop, axis=1, errors='ignore')
id_test = test['id'].values

del test
gc.collect()

# Build the model
cnt = 0
p_buf = []
n_splits = 5
n_repeats = 1
kf = RepeatedKFold(
    n_splits=n_splits, 
    n_repeats=n_repeats, 
    random_state=0)
auc_buf = []   

# load model to predict
try:
    import cPickle as pickle
except BaseException:
    import pickle
    

print('Load model to predict')
imported_model = pickle.load( open( "model_v1.pkl", "rb" ) )
print('model loaded')
#predict
results = imported_model.predict(X_test)
results