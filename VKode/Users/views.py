from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from . import forms


class LoginUser(LoginView):
    form_class = forms.UserLogin
    template_name = 'users/login.html'


class RegisterUser(CreateView):
    form_class = forms.UserRegistration
    template_name = 'users/register.html'


def logout_user(request: HttpRequest) -> HttpResponse:
    return HttpResponse('logout')

