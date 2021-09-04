from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class NotesCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create','get_html_image', 'is_published')
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (AdditionalImageInline,)

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50px>")

    get_html_image.short_description = 'Миниатюра'

admin.site.register(NotesCategory, NotesCategoryAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Reminder)
admin.site.register(AdvUser)
