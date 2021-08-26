from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy
from easy_thumbnails.files import get_thumbnailer

from .utils import get_timestamp_path


class NotesCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='User', default=1)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:notes_by_category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Note(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст записки')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Основное изображение')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован?')
    category = models.ForeignKey(NotesCategory, on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='User')

    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            # удаление всех миниатюр
            thumbnailer = get_thumbnailer(ai.image)
            thumbnailer.delete_thumbnails()
            # удаление изображения
            ai.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:show_note', kwargs={'note_slug': self.slug})

    class Meta:
        verbose_name = 'Записка'
        verbose_name_plural = 'Записки'


class AdditionalImage(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='Записка')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'


class Reminder(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст напоминания')
    is_once = models.BooleanField(default=True, verbose_name='Однократое напоминание?')
    date_cron = models.DateTimeField(blank=True,null=True, verbose_name='Дата_время напоминания')
    raw_cron = models.CharField(blank=True, max_length=50, verbose_name='Крон выражение напоминания')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='User')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('main:show_note', kwargs={'note_slug': self.slug})
    #
    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'
