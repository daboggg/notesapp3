from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, ValidationError
from django.contrib import messages

from main.models import Note, AdditionalImage, Reminder, NotesCategory, AdvUser, AdditionalFile
from PIL import Image
from .utils import date_range
import re
from notesapp.settings import CRON_REGEX


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TextInput):
    input_type = 'time'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TestForm(forms.Form):
    CHOICES = [('first', '111'),
               ('second', '222')]

    my_date_field = forms.DateField(widget=DateInput(attrs={'min': '2021-01-01', 'max': '2030-01-01'}))
    my_tyme_field = forms.TimeField(widget=TimeInput)


# форма добавления напоминания
class AddReminderForm(forms.ModelForm):
    date = date_range()
    date_cron = forms.DateTimeField(required=False, label='Дата-время напоминания', widget=DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'min': date['start'], 'max': date['finish']}))
    # date_cron = forms.DateField(widget=DateInput(attrs={'min': '2021-01-01', 'max': '2030-01-01'}))
    content = forms.CharField(label='Текст напоминания', required=False, widget=CKEditorWidget())

    def clean_raw_cron(self):
        if self.cleaned_data['raw_cron']:
            raw_cron = self.cleaned_data['raw_cron'].strip()
            if re.fullmatch(CRON_REGEX, raw_cron):
                return self.cleaned_data['raw_cron']
            else:
                raise ValidationError('неправильное выражение')
        return self.cleaned_data['raw_cron']

    class Meta:
        model = Reminder
        fields = ['title', 'content', 'is_once', 'date_cron', 'raw_cron' ]


# форма добавления записки
class AddNoteForm(forms.ModelForm):

    content = forms.CharField(required=False, widget=CKEditorWidget())

    MIN_RESOLUTION = (200, 200)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = NotesCategory.objects.filter(user=user)
        self.fields['image'].help_text = 'Загружайте изображение с минимальным разрешением {}x{}'.format(*self.MIN_RESOLUTION)

    def clean_image(self):
        if self.cleaned_data['image']:
            image = self.cleaned_data['image']
            img = Image.open(image)
            min_height, min_width = self.MIN_RESOLUTION
            if img.height < min_height or img.width < min_width:
                raise ValidationError('Разрешение изображения меньше минимального!')
            return image


    class Meta:
        model = Note
        fields = ['category', 'title', 'content', 'image', 'is_published', ]


AIFormSet = inlineformset_factory(Note, AdditionalImage, fields='__all__')


AFFormSet = inlineformset_factory(Note, AdditionalFile, fields='__all__')


# форма добавления категории
class AddNotesCategoryForm(forms.ModelForm):

    class Meta:
        model = NotesCategory
        fields = ['name']



#####################################################################################
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput())
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput())


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    first_name = forms.CharField(required=False, label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(required=False, label='Фамилия', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class ChangeUserinfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label= 'Aдpec электронной почты')
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name')
