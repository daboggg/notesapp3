from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, ValidationError
from django.contrib import messages

from main.models import Note, AdditionalImage
from PIL import Image


class AddNoteForm(forms.ModelForm):

    MIN_RESOLUTION = (200, 200)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображение с минимальным разрешением {}x{}'.format(*self.MIN_RESOLUTION)

    def clean_image(self):
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
