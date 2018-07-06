import pickle

def load_top_tens():
    files = ['project_title_tfidf_scores_top_ten.pk',
     'project_essay_tfidf_scores_top_ten.pk',
     'project_resource_summary_tfidf_scores_top_ten.pk']
    top_ten = {}

    for file in files:
        key = file[:-11]
        with open(file, 'rb') as f:
            top_ten[key] = pickle.load(f)
    return top_ten