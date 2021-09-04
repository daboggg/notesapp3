from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.management import BaseCommand
from datetime import datetime

from django.template.loader import render_to_string

from main.utils import delete_reminder
from notesapp import settings

from main.models import Reminder


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        id = kwargs.get('id')
        try:
            r = Reminder.objects.get(pk=id)
        except Reminder.DoesNotExist:
            return

        context={'r': r}
        s = render_to_string('email/mail.html', context)
        try:
            em = EmailMultiAlternatives(subject=r.title, body=r.content,from_email=settings.DEFAULT_FROM_EМAIL, to=[r.user.email])
            em.attach_alternative(s, 'text/html')
            em.send()
        except Exception as e:
            with open('two.txt', 'a') as file:
                file.write(str(e))

        if r.is_once:
            delete_reminder(id)
            r.delete()


        # ml = send_mail(
        #     r.title,
        #     r.content,
        #     settings.DEFAULT_FROM_EМAIL,
        #     [r.user.email],
        #     fail_silently=False,
        #     html_message=s
        # )



        # with open('two.txt', 'a') as file:
        #     file.write(f'{str(ml)}\n')

        # if ml:
        #     if r.is_once:
        #         delete_reminder(id)
        #         r.delete()



