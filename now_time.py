from datetime import datetime

def the_time():
    '''
    Take no input, process the current time for that feature of the application
    '''

    now = datetime.now()
    timedict = {
        'now': now,
        'year': int(now.strftime('%Y')),
        'month': int(now.strftime('%m')),
        'date': int(now.strftime('%d')),
        'day_of_week': int(now.strftime('%w')),
        'hour': int(now.strftime('%H')),
        'minute': int(now.strftime('%M'))
    }
    return timedict