from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from keras.preprocessing import sequence, text
from keras.layers import Input, Embedding

from nltk import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

import datetime as dt
import pandas as pd
import numpy as np
import warnings
import string

import matplotlib.pyplot as plt


stop_words = list(set(stopwords.words('english')))
warnings.filterwarnings('ignore')
punctuation = string.punctuation
# declare some strings
id_column = 'id'
missing_token = ' UNK '

# read in our data, parse_dates=['column name'] will read that column as a datetime object, can take a boolean, list of integers / names, list of lists or a dictionary,
# does different things depending on which one you use read the docs~
train = pd.read_csv('H:/uci_data/donorschoose-application-screening/train/train.csv', parse_dates=['project_submitted_datetime'])
test = pd.read_csv('H:/uci_data/donorschoose-application-screening/test/test.csv', parse_dates=['project_submitted_datetime'])
hopes = pd.read_csv('H:/uci_data/donorschoose-application-screening/resources/resources.csv').fillna(missing_token)

# lets make a master df of the train and test data to make our lives easier!
df = pd.concat([train,test], axis=0)
# A new column for total price
hopes['total_price'] = hopes['quantity']*hopes['price']

# Make an aggregate df to join to our normal df
# the .agg method takes in a function, string, or a dictionary or list of strings or functions.  The dictionary keys will be column names upon which functions should be run
# I named it after the horse in Shadow of the Colossus~ the description column is now a count of how many, so it can be renamed to (number of )items
agro = {'description':'count', 'quantity':'sum', 'price':'sum', 'total_price':'sum'}
aggregatedf = hopes.groupby('id').agg(agro).rename(columns={'description':'items'})

# now lets use that string functionality of .agg to get the min, max, and mean values!
for maths in ['min', 'max', 'mean']:
    # romanized Japanese horse name from game, and that guy that changes names in ff because why not lets have fun with variable names they're just for here anyway
    aguro = {'quantity':maths, 'price':maths, 'total_price':maths}
    namingway = {'quantity':maths+'_quantity', 'price':maths+'_price', 'total_price':maths+'_total_price'}
    
    # do some aggregation and join it to our previously created df
    temporary = hopes.groupby('id').agg(aguro).rename(columns=namingway).fillna(0)
    aggregatedf = aggregatedf.join(temporary)
# This didn't work whoops # aggregatedf = aggregatedf.join([hopes.groupby('id').agg({'quantity':maths, 'price':maths, 'total_price':maths}).rename(columns={'quantity':maths+'_quantity', 'price':maths+'_price', 'total_price':maths+'_total_price'}).fillna(0) for maths in ['min', 'max', 'mean']])

# and finally give it the original description columns aggregated together with a space in between them
aggregatedf = aggregatedf.join(hopes.groupby('id').agg({'description':lambda x:' '.join(x.values.astype(str))}).rename(columns={'description':'resource_description'}))

# Join that together with our everything df and check it out
df = df.join(aggregatedf, on='id')
# using datetime to make the above features
df['Year'] = df['project_submitted_datetime'].dt.year
df['Month'] = df['project_submitted_datetime'].dt.month
df['Year_Day'] = df['project_submitted_datetime'].dt.dayofyear
df['Month_Day'] = df['project_submitted_datetime'].dt.day
df['Week_Day'] = df['project_submitted_datetime'].dt.weekday
df['Hour'] = df['project_submitted_datetime'].dt.hour

# fill empty values with missing token ' UNK '
df['project_essay_3'] = df['project_essay_3'].fillna(missing_token)
df['project_essay_4'] = df['project_essay_4'].fillna(missing_token)

# get length of each essay and its title
df['essay1_len'] = df['project_essay_1'].apply(len)
df['essay2_len'] = df['project_essay_2'].apply(len)
df['essay3_len'] = df['project_essay_3'].apply(len)
df['essay4_len'] = df['project_essay_4'].apply(len)
df['title_len'] = df['project_title'].apply(len)

# Combine the essays into one string
df['text'] = df.apply(lambda row: ' '.join([str(row['project_essay_1']),
                                            str(row['project_essay_2']),
                                            str(row['project_essay_3']),
                                            str(row['project_essay_4'])]), axis=1)

# get our delicious features from that massive text
df['char_count'] = df['text'].apply(len)
df['word_count'] = df['text'].apply(lambda x: len(x.split()))
df['word density'] = df['char_count'] / (df['word_count'] + 1)
df['punctuation_count'] = df['text'].apply(lambda x: len("".join(_ for _ in x if _ in punctuation)))
df['title_word_count'] = df['text'].apply(lambda x: len([word for word in x.split() if word.istitle()]))
df['upper_case_word_count'] = df['text'].apply(lambda x: len([word for word in x.split() if word.isupper()]))
df['stopword_count'] = df['text'].apply(lambda x: len([word for word in x.split() if word.lower() in stop_words]))

# functions get polarity and subjectivity using TextBlob
def get_polarity(text):
    try:
        textblob = TextBlob(unicode(text, 'utf-8'))
        pol = textblob.sentiment.polarity
    except:
        pol = 0.0
    return pol

def get_subjectivity(text):
    try:
        textblob = TextBloob(unicode(text, 'utf-8'))
        subj = textblob.sentiment.subjectivity
    except:
        subj = 0.0
    return subj

# Now lets apply those functions to our df
df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)

pos_dict = {
    'noun': ['NN', 'NNS', 'NNP', 'NNPS'], #singular, plural regular nouns, singular, plural proper nouns
    'pron': ['PRP', 'PRP$', 'WP', 'WP$'], #personal pronouns, possessive personal, wh pronouns, possessive wh pronouns
    'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'], #verb base, past tense, gerund, past participle, singular present, 3rd person present
    'adj': ['JJ', 'JJR', 'JJS'], #adjective, comparative, superlative
    'adv': ['RB', 'RBR', 'RBS', 'WRB'] #adverb, compartive, superlative, wh- adverb
}

# function to retrieve the parts of speech tag counts
def pos_check(x, flag):
    cnt = 0
    try:
        wiki = TextBlob(x)
        for tup in wiki.tags:
            ppo = list(tup)[1]
            if ppo in pos_dic[flag]:
                cnt += 1
    except:
        pass
    return cnt

# now lets use that function to make new columns each in their own cell because it takes a while
df['noun_count'] = df['text'].apply(lambda x: pos_check(x, 'noun'))

df['verb_count'] = df['text'].apply(lambda x: pos_check(x, 'verb'))

df['adv_count'] = df['text'].apply(lambda x: pos_check(x, 'adv'))

df['pron_count'] = df['text'].apply(lambda x: pos_check(x, 'pron'))

df['resource_text'] = df.apply(lambda row: ' '.join([str(row['resource_description']), str(row['project_resource_summary'])]), axis=1)

article_text = list(df['text'].values)
title_text = list(df['project_title'].values)
resource_text = list(df['resource_text'].values)

df.to_csv('H:/uci_data/donorschoose-application-screening/everything.csv')

# make tfidf and save them
import pickle
def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# word level tf-idf for article text
vectorizer = TfidfVectorizer(max_features=2500, analyzer='word', stop_words='english', ngram_range=(1,3), dtype=np.float32)
vectorizer.fit(article_text)
article_word_tfidf = vectorizer.transform(article_text)

save_obj(article_word_tfidf, 'article_word_tfidf')


# word level tf-idf for titles
vectorizer = TfidfVectorizer(max_features=2500, analyzer='word', stop_words='english', ngram_range=(1,3), dtype=np.float32)
vectorizer.fit(title_text)
title_word_tfidf = vectorizer.transform(title_text)
save_obj(title_word_tfidf, 'title_word_tfidf')

# word level tf-idf for resource text
vectorizer = TfidfVectorizer(max_features=2500, analyzer='word', stop_words='english', ngram_range=(1,3), dtype=np.float32)
vectorizer.fit(resource_text)
resource_word_tfidf = vectorizer.transform(resource_text)
save_obj(resource_word_tfidf, 'resource_word_tfidf')


# create a dictionary mapping tokens to their tfidf values
tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
tfidf = pd.DataFrame(columns=['resource_word_tfidf']).from_dict(dict(tfidf), orient='index')
tfidf.columns = ['resource_word_tfidf']



# 15 highest tf-idf from that list
tfidf.sort_values(by=['resource_word_tfidf'], ascending=False).head(15)
save_obj(tfidf, 'tfidf')
