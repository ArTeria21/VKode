from django.urls import path
from . import views
from .views import CustomTokenObtainPairView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "users"

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/profile/", UserProfileView.as_view(), name="user_profile"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("registration/", views.RegisterUser.as_view(), name="registration"),
    path("logout/", views.logout_user, name="logout"),
]
