from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class UserRegistration(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput())
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput())
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserLogin(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput())