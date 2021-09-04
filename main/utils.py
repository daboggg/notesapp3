from os.path import splitext
from datetime import datetime
from dateutil.relativedelta import relativedelta
from crontab import CronTab
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer
from django.template.loader import render_to_string

from notesapp import settings
from notesapp.settings import BASE_DIR, ALLOWED_HOSTS


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


signer = Signer()

def send_activation_notification(user, request):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host,
               'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    body_html = render_to_string('email/activation_letter_body.html', context)


    try:
        em = EmailMultiAlternatives(subject=subject, body=body_text, from_email=settings.DEFAULT_FROM_EМAIL,
                                    to=[user.email])
        em.attach_alternative(body_html, 'text/html')
        em.send()
        messages.add_message(request, messages.SUCCESS, f'На {user.email} отправлено сообщение')
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)