from datetime import datetime

def what_time_is_it_mr_wolf():
    now = datetime.now()
    timedict = {
        'year': int(now.strftime('%Y')),
        'month': int(now.strftime('%m')),
        'date': int(now.strftime('%d')),
        'day_of_week': int(now.strftime('%w')),
        'hour': int(now.strftime('%H')),
        'minute': int(now.strftime('%M'))
    }
    return timedict