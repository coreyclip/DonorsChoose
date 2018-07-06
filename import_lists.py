import pickle

def import_lists():
    '''
    This function takes in no inputs, but outputs the dropdown menu lists for the front end to populate
    '''
    with open('dropdownpop.pk', 'rb') as f:
        lists = pickle.load(f)
    return lists