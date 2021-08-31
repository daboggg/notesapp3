from django.apps import AppConfig
from django.dispatch import Signal, receiver


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Заметки и напоминалки'


# test_sngl = Signal(providing_args=['test'])
#
# @receiver(test_sngl)
# def test_sngl_dispatcher(sender, **kwargs):
#     pass
