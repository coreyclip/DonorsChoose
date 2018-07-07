
def user_report(user_input):
    grade_report = ""
    subject_report = ""
    essay_report = ""
    
    print(user_input)
    
    total_wc = user_input["project_essay_1_wc"] + user_input["project_essay_2_wc"] + user_input["project_essay_3_wc"] + user_input["project_essay_4_wc"]
    
    average_wc = round(total_wc/4, 2)
    
    try:
        subject = user_input["project_subject_categories"]
        if subject in ['Literacy & Language', "Math & Science", "Health & Sports"]:
            subject_report += f"""
                your subject {subject} is in the top three most common categories applicants apply for, 
                subjects that are not in the top three: Health & Sports, Math & Science, Literacy & Language have
                a slightly higher chance of being approved, though by listing a sub category this penalty is mostly nullified
                """
        else:
            subject_report += f"""
            your subject {subject} is not in one of the the the top three subject catregories:
            Health & Sports, Math & Science, or Literacy & Language,
            subjects other than these have a slighly higher chance of being approved
            providing a sub-category as well also increases your chances
            """
    except:
        subject_report += f"""
            your subject is not in one of the the the top three subject catregories:
            Health & Sports, Math & Science, or Literacy & Language,
            subjects other than these have a slighly higher chance of being approved
            providing a sub-category as well also increases your chances
            """
    try:        
        if user_input["project_grade_category"] == "Grades 3-5":
            grade_report += """ Projects submitted for the 3rd to 5th grades have the
            highest acceptance rate compared to other categories. Most projects tend to be
            geared towards younger students. 70k projects were submitted for pre-k to 2nd grade students 
            vs. 17k for high school students. 
            """
        elif user_input["project_grade_category"] == "Grades 9-12":
            grade_report += """ Projects submitted for High School students have a slightly
            lower chance of being funded. This is in part because their projects are generally
            more expensive.
            """
        else:
            grade_report += """ Most projects tend to be
            geared towards younger students. 70k projects were submitted for pre-k to 2nd grade students 
            vs. 17k for high school students. """
    except:
        grade_report += """ Most projects tend to be
            geared towards younger students. 70k projects were submitted for pre-k to 2nd grade students 
            vs. 17k for high school students. """
    try:   
        essay_report = f""" As it should, your essays are the most important part of your 
        application. Giving descriptive and well thought out essays is the best way to make 
        your application stand out. Applicantions that are approved typically have about 5-7 words
        in their titles with some higher, your title has {user_input["project_title_wc"]} words, based on raw
        correlations this gives your application a {round((user_input["project_title_wc"] * 0.21),2) * 100}% boost. 
        Your essays have an average of {average_wc} words each. Successful essays typically have word counts from 110 to 150.
        
        """
    except:
        essay_report = f""" As it should, your essays are the most important part of your 
        application. Giving descriptive and well thought out essays is the best way to make 
        your application stand out. Applicantions that are approved typically have about 5-7 words
        in their titles with some higher. Successful essays typically have word counts from 110 to 150.
        
        """

    return essay_report, grade_report, subject_report