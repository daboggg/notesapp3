from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from main.form import LoginUserForm


def index(request):
    return render(request, 'main/index.html')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('main:index')

def logout_user(request):
    logout(request)
    return redirect('main:login')