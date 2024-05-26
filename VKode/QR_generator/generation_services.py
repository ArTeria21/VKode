import segno
from datetime import datetime
from random import randint
import hashlib
from .apps import REDIRECT_PATH
from .models import QRCode
from django.http import HttpRequest

def count_qr_code_hash(username: str, code_name: str) -> int:
    return hashlib.sha3_256(f'{username} {code_name}'.encode()).hexdigest()

def create_redirect_url(code_hash: str) -> str:
    return f'{REDIRECT_PATH}/{code_hash}/'

def generate_qr_code(direction: str) -> str:
    '''Функция для создания QR-кода.

    Принимает URL, который нужно закодировать
    Возвращает путь к QR коду
    '''
    qrcode = segno.make_qr(direction)

    date = datetime.now().date()
    hours = datetime.now().time().hour
    minutes = datetime.now().time().minute
    seconds = datetime.now().time().second
    random_number = randint(0, 1000)

    filename = f'{date}_{hours}_{minutes}_{seconds}_{random_number}_QR.png'
    file_path = f'/home/artem/College/RPM/VKode/VKode/qr_codes/{filename}'
    qrcode.save(file_path,
                scale=10)
    return file_path

def create_redirect_code(username, code_name) -> tuple[str]:
    code_hash = count_qr_code_hash(username, code_name)
    link = create_redirect_url(code_hash)
    qr_path = generate_qr_code(link)
    return code_hash, qr_path

def create_list_of_codes(request: HttpRequest) -> list[dict]:
    user = request.user
    username = user.username
    qr_codes = QRCode.objects.filter(owner=user)
    params_to_dashboard = []
    for code in qr_codes:
        temporary = {'code_name':code.code_name,
                    'direction':code.direction,
                    'category':code.category,
                    'end_time':code.end_time,
                    }
        params_to_dashboard.append(temporary)
    return params_to_dashboard