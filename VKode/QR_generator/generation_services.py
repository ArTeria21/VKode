import segno
from datetime import datetime
from random import randint


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

