import pickle

def import_lists():
    '''
    Load the value lists for our dropdowns for the frontend
    '''
    with open('dropdownpop.pk', 'rb') as f:
        lists = pickle.load(f)
    return lists