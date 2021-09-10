from django.urls import path

from .views import *

app_name = 'main'

urlpatterns =[
    path('', index, name='index'),
    path('aa/', mail, name='mail'),
    path('addnotescategory/', AddNotesCategory.as_view(), name='addnotescategory'),
    path('addnote/', AddNote.as_view(), name='addnote'),
    path('addreminder/', AddReminder.as_view(), name='addreminder'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('notes/', Notes.as_view(), name='notes'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('reminders/', Reminders.as_view(), name='reminders'),
    path('test/', test, name='test'),
    path('deletenote/<slug:note_slug>/', DeleteNote.as_view(), name='deletenote'),
    path('deletereminder/<slug:reminder_slug>/', DeleteReminder.as_view(), name='deletereminder'),
    path('deletenotecategory/<slug:cat_slug>/', DeleteCategory.as_view(), name='deletenotecategory'),
    path('note/<slug:note_slug>/', ShowNote.as_view(), name='show_note'),
    path('reminder/<slug:reminder_slug>/', ShowReminder.as_view(), name='show_reminder'),
    path('updatenote/<slug:note_slug>/', UpdateNote.as_view(), name='updatenote'),
    path('updatereminder/<slug:reminder_slug>/', UpdateReminder.as_view(), name='updatereminder'),
    path('notes_by_category/<slug:cat_slug>/', NotesByCategory.as_view(), name='notes_by_category'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/repeat/activate/', send_repeat_email_activation, name='repeat_activate'),
    path('change/user/info/', ChangeUserInfoView.as_view(), name='change_user_info'),
    path('change/user/password/', AppPasswordChangeView.as_view(), name='change_user_password'),
]
