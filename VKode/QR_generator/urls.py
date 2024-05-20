from django.urls import path
from django.contrib.auth import views as auth_views
from .authentication.auth_views import signup_view
import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create/', views.create_qr_code, name='create_code'),
    path('dashboard/', views.dashboard, name='dashboard'),
]