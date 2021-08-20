from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from main.models import Note, AdditionalImage


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['category', 'title', 'content', 'image', 'is_published', ]


AIFormSet = inlineformset_factory(Note, AdditionalImage, fields='__all__')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput())
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput())


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
