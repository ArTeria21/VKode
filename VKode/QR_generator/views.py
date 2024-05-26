# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from .forms import CreateQRCodeForm
from .models import QRCode, Category, Transition
from .generation_services import create_redirect_code, create_list_of_codes
import hashlib
from datetime import datetime

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

            # Генерация QR кода, получение пути к файлу и хеша
            code_hash, path_to_file = create_redirect_code(user.username, code_name)

            # Создание записи о QR коде в базе данных
            qr_code = QRCode.objects.create(
                code_name=code_name,
                owner=user,
                direction=direction,
                category=Category.objects.get(id=category_id) if category_id else None,
                end_time=end_time,
                path_to_file=path_to_file,
                code_hash=code_hash
            )

            return redirect('dashboard')  # Перенаправляем на страницу дашборда после успешного создания
    else:
        form = CreateQRCodeForm()
    data = {
        'title': 'Создание QR кода',
        'form': form
    }
    return render(request, 'generator/create_qr_code.html', context=data)

def redirect_page(request: HttpRequest, hash: str) -> HttpResponse:
    qr_code = get_object_or_404(QRCode, code_hash=hash)
    if not isinstance(qr_code, QRCode):
        return redirect(qr_code.direction)
    
    if qr_code.end_time and qr_code.end_time < timezone.now():
        return HttpResponse('Код больше не работает (((')
    
    Transition.objects.create(
    code=qr_code,
    user_agent=request.META['HTTP_USER_AGENT'],
    ip_address=request.META['REMOTE_ADDR'],
    )
    return redirect(qr_code.direction)


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    params_to_dashboard = create_list_of_codes(request)
    data = {
        'username' : request.user.username,
        'qr_codes': params_to_dashboard
    }
        
    return render(request, context=data, template_name='generator/dashboard.html')
