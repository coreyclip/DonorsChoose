import pickle

def import_lists():
    with open('dropdownpop.pk', 'rb') as f:
        lists = pickle.load(f)
    return lists