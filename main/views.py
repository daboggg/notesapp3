from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from main.form import *
from main.models import Note, Reminder
from slugify import slugify
from easy_thumbnails.files import get_thumbnailer
from datetime import datetime
from .utils import *


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница'})


###########################################################################
# НАПОМИНАНИЕ


# одно напоминание  детально
class ShowReminder(LoginRequiredMixin, DetailView):
    model = Reminder
    template_name = 'main/reminder.html'
    slug_url_kwarg = 'reminder_slug'
    context_object_name = 'reminder'
    extra_context = {'title': 'Напоминание'}

    def get_object(self, queryset=None):
        try:
            return Reminder.objects.get(slug=self.kwargs['reminder_slug'], user=self.request.user)
        except Exception:
            raise Http404('Нет такого напоминания')

# Все напоминания по авторизованому пользователю
class Reminders(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Reminder
    context_object_name = 'reminders'
    template_name = 'main/reminders.html'
    extra_context = {'title': 'Напоминания'}

    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)


# добавление напоминания
class AddReminder(LoginRequiredMixin, CreateView):
    form_class = AddReminderForm
    template_name = 'main/addreminder.html'
    extra_context = {'title': 'Добавление напоминания'}
    success_url = reverse_lazy('main:reminders')



    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = self.request.user
        fields.slug = f'{slugify(fields.title)}-{slugify(str(datetime.now()))}'
        fields.save()
        add_reminder(fields)
        # print(isinstance(fields.date_cron, datetime))
        return super().form_valid(form)


# удаление напоминания
class DeleteReminder(LoginRequiredMixin, DeleteView):
    model = Reminder
    slug_url_kwarg = 'reminder_slug'
    success_url = reverse_lazy('main:reminders')
    extra_context = {'title': 'Удаление напоминания'}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            # удаление записки
            delete_reminder(self.object.id)
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(request, messages.ERROR, 'Удаление не возможно, это не вашe напоминание')
            return HttpResponseRedirect(self.success_url)

###########################################################################
# ЗАПИСКА

# Все записки по авторизованому пользователю
class Notes(LoginRequiredMixin, ListView):
    paginate_by = 10
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
class NotesByCategory(LoginRequiredMixin, ListView):
    paginate_by = 10
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
class ShowNote(LoginRequiredMixin, DetailView):
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


# добавление записки
class AddNote(LoginRequiredMixin, CreateView):
    form_class = AddNoteForm
    template_name = 'main/addnote.html'

    # success_url = reverse_lazy('main:notes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = User.objects.get(pk=self.request.user.pk)
        fields.slug = f'{slugify(fields.title)}-{slugify(str(datetime.now()))}'
        fields.save()
        formset = AIFormSet(self.request.POST, self.request.FILES, instance=fields)
        if formset.is_valid():
            formset.save()
            messages.add_message(self.request, messages.SUCCESS, 'Записка добавлена')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = AIFormSet()
        context['title'] = 'Добавление записки'
        return context


# редактирование записки
class UpdateNote(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = AddNoteForm
    template_name = 'main/updatenote.html'
    slug_url_kwarg = 'note_slug'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Note.objects.filter(slug=self.kwargs[self.slug_url_kwarg], user=self.request.user)

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = self.request.user
        # fields.slug = f'{slugify(fields.title)}-{slugify(str(datetime.now()))}'
        fields.save()
        formset = AIFormSet(self.request.POST, self.request.FILES, instance=fields)
        print(self.request.POST)
        if formset.is_valid():
            formset.save()
            messages.add_message(self.request, messages.SUCCESS, 'Записка исправлена')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = AIFormSet(instance=self.object)
        context['title'] = 'Редактирование записки'
        return context


# удаление записки
class DeleteNote(LoginRequiredMixin, DeleteView):
    model = Note
    slug_url_kwarg = 'note_slug'
    success_url = reverse_lazy('main:notes')
    extra_context = {'title': 'Удаление записки'}

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:

            # удаление всех миниатюр
            thumbnailer = get_thumbnailer(self.object.image)
            thumbnailer.delete_thumbnails()
            # удаление записки
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(request, messages.ERROR, 'Удаление не возможно, это не ваша записка')
            return HttpResponseRedirect(self.success_url)



# добавление категории
class AddNotesCategory(LoginRequiredMixin, CreateView):
    form_class = AddNotesCategoryForm
    template_name = 'main/addnotescategory.html'
    extra_context = {'title': 'Добавление категории'}
    success_url = reverse_lazy('main:notes')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user = self.request.user
        fields.slug = f'{slugify(fields.name)}-{slugify(str(datetime.now()))}'
        fields.save()
        return super().form_valid(form)



#######################################################################################
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


###############################################################################
# тесты
def mail(request):
    ml = send_mail(
        'Subject here',
        'Here is the message.',
        'v.zinin@rambler.ru',
        ['vzinin@list.ru'],
        fail_silently=False,
    )
    print(ml)
    return render(request, 'main/index.html')


def test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = TestForm()
    return render(request, 'main/test.html', {'form': form})