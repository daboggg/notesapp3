from os.path import splitext
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

# возващает текущую дату-время и текущую дату-время плюс 10 лет
def date_range():
    now = datetime.now()
    start = now.strftime('%Y-%m-%dT%H:%M')
    finish = now + relativedelta(years=10)
    return {'start': start, 'finish': finish.strftime('%Y-%m-%dT%H:%M')}