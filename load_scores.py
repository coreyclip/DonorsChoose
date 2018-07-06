import pickle

def load_scores():
    files = [
        'project_title_tfidf_scores',
        'project_essay_tfidf_scores',
        'project_resource_summary_tfidf_scores'
    ]
    scores = {}
    for file in files:
        filename = file + '.pk'
        with open(filename, 'rb') as f:
            scores[file] = pickle.load(f)
    return scores