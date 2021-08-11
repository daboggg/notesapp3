from django.contrib import admin

from .models import *

class NotesCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(NotesCategory, NotesCategoryAdmin)
admin.site.register(Note)
