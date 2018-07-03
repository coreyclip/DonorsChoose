import pickle
import pandas as pd
import numpy as np

with open('model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

def PREDICTABO(data):
    '''
    Geese Howard says PREDICTABO a lot.  Anyway, this will read in our data and make a prediction
    '''
    data = pd.DataFrame.from_dict(data)
    data['teacher_number_of_previously_posted_projects'] = data['teacher_number_of_previously_posted_projects'].astype(int)
    data['project_submitted_datetime'] = pd.to_datetime(data['project_submitted_datetime']).values.astype(np.int64)
    return model.predict(data, num_iteration=model.best_iteration)