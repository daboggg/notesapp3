from django.urls import path

from .views import *

app_name = 'main'

urlpatterns =[
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('notes/', Notes.as_view(), name='notes'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('', index, name='index'),
]