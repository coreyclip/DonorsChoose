import json
import lightgbm as lgb
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

try:
    import cPickle as pickle
except BaseException:
    import pickle

# load model to predict
print('Load model to predict')
lgb = lgb.Booster(model_file='lgb.txt')
print('model loaded')