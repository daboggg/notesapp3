from django.urls import path

from .views import *

app_name = 'main'

urlpatterns =[
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('', index, name='index'),
]