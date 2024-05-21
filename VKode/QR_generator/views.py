from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .forms import CreateQRCodeForm
from .models import QRCode, Category
from .generation_services import generate_qr_code
import os


def index(request: HttpRequest) -> HttpResponse:
    return render(request, template_name='generator/index.html')

@login_required
def create_qr_code(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateQRCodeForm(request.POST)
        if form.is_valid():
            code_name = form.cleaned_data['code_name']
            direction = form.cleaned_data['direction']
            category_id = form.cleaned_data.get('category')
            end_time = form.cleaned_data.get('end_time')

            # Получаем текущего пользователя
            user = request.user
            client = get_user_model().objects.get(user=user)

            # Генерация QR кода и получение пути к файлу
            path_to_file = generate_qr_code(direction)

            # Создание записи о QR коде в базе данных
            qr_code = QRCode.objects.create(
                code_name=code_name,
                owner=client,
                direction=direction,
                category=Category.objects.get(id=category_id) if category_id else None,
                end_time=end_time,
                path_to_file=path_to_file
            )

            return HttpResponse(request, {'status':'success'})  # Перенаправляем на страницу успешного создания
    else:
        form = CreateQRCodeForm()
    data = {
        'title': 'Создание QR кода',
        'form': form
    }
    return render(request, 'generator/create_qr_code.html', context=data)

def dashboard(request: HttpRequest) -> HttpResponse:
    return HttpResponse('dashboard')
