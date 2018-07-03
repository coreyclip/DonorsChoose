import pickle
import pandas as pd

with open('model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

def PREDICTABO(data):
    return model.predict(data)