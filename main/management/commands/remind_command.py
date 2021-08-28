from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        id = kwargs.get('id')
        with open('two.txt', 'a') as file:
            file.write(str(id))
        print(id)