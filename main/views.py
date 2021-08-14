from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from main.form import LoginUserForm, RegisterUserForm, AddNoteForm
from main.models import Note
from slugify import slugify


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


# def notes(request):
#     return render(request, 'main/notes.html', {'title': 'Заметки'})


# Все записки по авторизованому пользователю
class Notes(ListView, LoginRequiredMixin):
    model = Note
    context_object_name = 'notes'
    template_name = 'main/notes.html'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


    def get_context_data(self, **kwargs):
        # print(dir(self.request.user))
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записки'
        context['cat_selected'] = ''
        return context


# Все записки по авторизованому пользователю и выбранной категории
class NotesByCategory(ListView, LoginRequiredMixin):
    model = Note
    context_object_name = 'notes'
    template_name = 'main/notes.html'

    def get_queryset(self):
        return Note.objects.filter(category__slug=self.kwargs['cat_slug'], user=self.request.user)

    def get_context_data(self, **kwargs):
        # print(dir(self.request.user))
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записки - ' + str(context['notes'][0].category)
        context['cat_selected'] = self.kwargs['cat_slug']
        return context


# одна записка детально
class ShowNote(DetailView):
    model = Note
    template_name = 'main/note.html'
    slug_url_kwarg = 'note_slug'
    context_object_name = 'note'
    extra_context = {'title': 'Запискa'}

    def get_object(self, queryset=None):
        try:
            return Note.objects.get(slug=self.kwargs['note_slug'], user=self.request.user)
        except Exception:
            raise Http404('Нет такой записки')


class AddNote(LoginRequiredMixin, CreateView):
    form_class = AddNoteForm
    template_name = 'main/addnote.html'
    success_url = reverse_lazy('main:notes')


    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user =User.objects.get(pk=self.request.user.pk)
        fields.slug = slugify(fields.title)
        fields.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление записки'
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