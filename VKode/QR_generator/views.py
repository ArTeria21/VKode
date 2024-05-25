# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .forms import CreateQRCodeForm
from .models import QRCode, Category
from .generation_services import generate_qr_code
import hashlib

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
            code_hash = hashlib.sha3_256(f'{user.username} {code_name}'.encode()).hexdigest()

            redirect_path = f'http://127.0.0.1:8000/code/{code_hash}/'
            # Генерация QR кода и получение пути к файлу
            path_to_file = generate_qr_code(redirect_path)

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
    return redirect(qr_code.direction)

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return HttpResponse('dashboard')
