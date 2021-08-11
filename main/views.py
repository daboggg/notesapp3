from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from main.form import LoginUserForm, RegisterUserForm
from main.models import Note


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


# def notes(request):
#     return render(request, 'main/notes.html', {'title': 'Заметки'})


# Все записки по авторизованому пользователю
class Notes(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'main/notes.html'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


    def get_context_data(self, **kwargs):
        # print(dir(self.request.user))
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записки'
        context['cat_selected'] = 'vsyakoe'
        return context


class NotesByCategory(ListView):
    model = Note
    template_name = 'main/notes.html'

    def get_context_data(self, **kwargs):
        # print(dir(self.request.user))
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записки'
        context['cat_selected'] = self.kwargs['cat_slug']
        return context


# Регистрация и авторизация
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('main:index')

def logout_user(request):
    logout(request)
    return redirect('main:login')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:index')