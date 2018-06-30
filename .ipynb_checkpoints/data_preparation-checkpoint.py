import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

dtype = {
    'id': str,
    'teacher_id': str,
    'teacher_prefix': str,
    'school_state': str,
    'project_submitted_datetime': str,
    'project_grade_category': str,
    'project_subject_categories': str,
    'project_subject_subcategories': str,
    'project_title': str,
    'project_essay_1': str,
    'project_essay_2': str,
    'project_essay_3': str,
    'project_essay_4': str,
    'project_resource_summary': str,
    'teacher_number_of_previously_posted_projects': int,
    'project_is_approved': np.uint8,
}

def prepare_data(prefix, state, date, grade, subject_cat, subject_subcat, title, essay_1, essay_2, essay_3, essay_4, resource_summary, previous_project_num):
    """
    Take in all of the information from our front end and prepare for algorithm insertion
    """
    # First let's just make it all a nice little dataframe
    df = pd.DataFrame({
        'teacher_prefix': prefix,
        'school_state': state,
        'project_submitted_datetime': date,
    'project_grade_category': grade,
    'project_subject_categories': subject_cat,
    'project_subject_subcategories': subject_subcat,
    'project_title': title,
    'project_essay_1': essay_1,
    'project_essay_2': essay_2,
    'project_essay_3': essay_3,
    'project_essay_4': essay_4,
    'project_resource_summary': resource_summary,
    'teacher_number_of_previously_posted_projects': previous_project_num,
    })

    # Join up the essays into one big essay
    df['project_essay'] = df.apply(lambda row: ' '.join([
        str(row['project_essay_1']),
        str(row['project_essay_2']),
        str(row['project_essay_3']),
        str(row['project_essay_4'])
        ]), axis = 1)
    
        df['project_title_len'] = df['project_title'].apply(lambda x: len(str(x)))
        df['project_essay_1_len'] = df['project_essay_1'].apply(lambda x: len(str(x)))
        df['project_essay_2_len'] = df['project_essay_2'].apply(lambda x: len(str(x)))
        df['project_essay_3_len'] = df['project_essay_3'].apply(lambda x: len(str(x)))
        df['project_essay_4_len'] = df['project_essay_4'].apply(lambda x: len(str(x)))
        df['project_resource_summary_len'] = df['project_resource_summary'].apply(lambda x: len(str(x)))

        df['project_title_wc'] = df['project_title'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_1_wc'] = df['project_essay_1'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_2_wc'] = df['project_essay_2'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_3_wc'] = df['project_essay_3'].apply(lambda x: len(str(x).split(' ')))
        df['project_essay_4_wc'] = df['project_essay_4'].apply(lambda x: len(str(x).split(' ')))
        df['project_resource_summary_wc'] = df['project_resource_summary'].apply(lambda x: len(str(x).split(' ')))
        