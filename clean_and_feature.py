
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
import collections

import matplotlib.pyplot as plt
%matplotlib inline

def blob_the_text(text):
    """
    take in a text and apply a bunch of text blob features to it
    INPUT: text string
    OUTPUT: a tuple of everything you might want textblob to run on that text
            sentiment polarity,
            sentiment subjectivity,
            count of nouns,
            count of pronouns,
            count of verbs,
            count of adjectives,
            count of adverbs
    """
    tb = TextBlob(text)

    nouns = ['NN', 'NNS', 'NNP', 'NNPS'] #singular, plural regular nouns, singular, plural proper nouns
    pronouns = ['PRP', 'PRP$', 'WP', 'WP$'] #personal pronouns, possessive personal, wh pronouns, possessive wh pronouns
    verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] #verb base, past tense, gerund, past participle, singular present, 3rd person present
    adjectives = ['JJ', 'JJR', 'JJS'] #adjective, comparative, superlative
    adverbs = ['RB', 'RBR', 'RBS', 'WRB'] #adverb, compartive, superlative, wh- adverb

    tagcol = collections.namedtuple('tag', ['word', 'pos'])
    tags = [tagcol(word[0], word[1]) for word in tb.tags]

    try:
        pol = tb.sentiment.polarity
    except:
        pol = 0.0
    try:
        subj = tb.sentiment.subjectivity
    except:
        subj = 0.0
    ncount = sum(collections.Counter(tag.pos for tag in tags if tag.pos in nouns).values())
    procount = sum(collections.Counter(tag.pos for tag in tags if tag.pos in pronouns).values())
    vcount = sum(collections.Counter(tag.pos for tag in tags if tag.pos in verbs).values())
    adjcount = sum(collections.Counter(tag.pos for tag in tags if tag.pos in adjectives).values())
    advcount = sum(collections.Counter(tag.pos for tag in tags if tag.pos in adverbs).values())

    # print('polarity {} subjectivity {}'.format(pol, subj))
    # print('pos tags: {}'.format(posstring))
    # trying = TextBlob(df['text'][0]).tags
    # tag = collections.namedtuple('tag', ['word', 'pos'])
    # tags = [tag(thing[0], thing[1]) for thing in trying]
    return [pol, subj, ncount, procount, vcount, adjcount, advcount]

stop_words = list(set(stopwords.words('english')))
warnings.filterwarnings('ignore')
punctuation = string.punctuation

# declare some strings
id_column = 'id'
missing_token = ' UNK '

# read in our data, parse_dates=['column name'] will read that column as a datetime object, can take a boolean, list of integers / names, list of lists or a dictionary,
# does different things depending on which one you use read the docs~
train = pd.read_csv('data/train.csv', parse_dates=['project_submitted_datetime'])
# test = pd.read_csv('data/test.csv', parse_dates=['project_submitted_datetime'])
hopes = pd.read_csv('data/resources.csv').fillna(missing_token)

# # lets make a master df of the train and test data to make our lives easier!
# df = pd.concat([train,test], axis=0)
# no lets not that was awful
df = train

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
df.head()

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

df[['polarity', 'subjectivity', 'noun_count', 'pronoun_count', 'verb_count', 'adjective_count', 'adverb_count']] = pd.DataFrame([(blob_the_text(row['text'])) for index, row in df.iterrows()], index = df.index)

df.to_csv('../data/training_clean.csv')