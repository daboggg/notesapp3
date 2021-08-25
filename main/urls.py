from django.urls import path

from .views import *

app_name = 'main'

urlpatterns =[
    path('', index, name='index'),
    path('aa/', mail, name='mail'),
    path('addnote/', AddNote.as_view(), name='addnote'),
    path('addreminder/', AddReminder.as_view(), name='addreminder'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('notes/', Notes.as_view(), name='notes'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('reminders/', Reminders.as_view(), name='reminders'),
    path('test/', test, name='test'),
    path('deletenote/<slug:note_slug>/', DeleteNote.as_view(), name='deletenote'),
    path('note/<slug:note_slug>/', ShowNote.as_view(), name='show_note'),
    path('updatenote/<slug:note_slug>/', UpdateNote.as_view(), name='updatenote'),
    path('notes_by_category/<slug:cat_slug>/', NotesByCategory.as_view(), name='notes_by_category'),
]
