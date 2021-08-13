from django.urls import path

from .views import *

app_name = 'main'

urlpatterns =[
    path('', index, name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('notes/', Notes.as_view(), name='notes'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('note/<slug:note_slug>/', ShowNote.as_view(), name='show_note'),
    path('notes_by_category/<slug:cat_slug>/', NotesByCategory.as_view(), name='notes_by_category'),
]