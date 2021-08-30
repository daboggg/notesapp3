from os.path import splitext
from datetime import datetime
from dateutil.relativedelta import relativedelta
from crontab import CronTab
from notesapp.settings import BASE_DIR


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])

# возващает текущую дату-время и текущую дату-время плюс 10 лет
def date_range():
    now = datetime.now()
    start = now.strftime('%Y-%m-%dT%H:%M')
    finish = now + relativedelta(years=10)
    return {'start': start, 'finish': finish.strftime('%Y-%m-%dT%H:%M')}


# добавляет запись в crontab
def add_reminder(fields):
    PYTHON_PATH = f'{BASE_DIR}/venv/bin/python'
    COMMAND_PATH = f'{BASE_DIR}/manage.py remind_command {fields.id}'

    with CronTab(user='daboggg') as cron:
        job = cron.new(command=f'{PYTHON_PATH} {COMMAND_PATH}', comment=f'{fields.id}')
        if fields.date_cron:
            job.setall(fields.date_cron)
        else:
            job.setall(fields.raw_cron)

# удаляет запись из crontab
def delete_reminder(id):
    with CronTab(user='daboggg') as cron:
        cron.remove_all(comment=str(id))
