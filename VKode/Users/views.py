from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserLogin, UserRegistration
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoginUser(LoginView):
    form_class = UserLogin
    template_name = "users/login.html"
    title = "Авторизация"

class RegisterUser(CreateView):
    form_class = UserRegistration
    template_name = "users/register.html"
    success_url = reverse_lazy("index")
    title = "Регистрация"

    def form_valid(self, form):
        response = super().form_valid(form)
        # Additional logic can be added here if needed
        return response

    def form_invalid(self, form):
        # Handle form errors
        return self.render_to_response(self.get_context_data(form=form))

def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("index")
