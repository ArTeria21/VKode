from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_qr_code, name="create_code"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("code/<str:hash>/", views.redirect_page, name="redirect"),
    path("statistics/<str:code_hash>/", views.qr_code_statistics, name="statistics"),
]
