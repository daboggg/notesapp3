from django.contrib.auth.models import User
from django.db import models

class NotesCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Note(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст записки')
    image = models.ImageField(upload_to='img/%Y/%m/%d/', verbose_name='Изображение')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован?')
    category = models.ForeignKey(NotesCategory, on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='User')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Записка'
        verbose_name_plural = 'Записки'

