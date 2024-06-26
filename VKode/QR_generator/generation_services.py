from django.conf import settings
import segno
from datetime import datetime
from random import randint
import hashlib
from .apps import REDIRECT_PATH
from .models import QRCode, Transition
from django.http import HttpRequest
import pandas as pd
import plotly.express as px
import plotly.io as pio

import os

def count_qr_code_hash(username: str, code_name: str) -> int:
    return hashlib.sha3_256(f"{username} {code_name}".encode()).hexdigest()


def create_redirect_url(code_hash: str) -> str:
    return f"{REDIRECT_PATH}/{code_hash}/"


def generate_qr_code(direction: str) -> str:
    """Функция для создания QR-кода.

    Принимает URL, который нужно закодировать
    Возвращает путь к QR коду
    """
    qrcode = segno.make_qr(direction)

    date = datetime.now().date()
    hours = datetime.now().time().hour
    minutes = datetime.now().time().minute
    seconds = datetime.now().time().second
    random_number = randint(0, 1000)

    filename = f"{date}_{hours}_{minutes}_{seconds}_{random_number}_QR.png"
    directory = os.path.join("media", "qr_codes")
    os.makedirs(directory, exist_ok=True)  # Создать директорию, если она не существует
    file_path = os.path.join(directory, filename)
    
    print(f"Saving QR code to: {file_path}")  # Вывод пути для отладки
    qrcode.save(file_path, scale=10)
    return file_path



def create_redirect_code(username, code_name) -> tuple[str]:
    code_hash = count_qr_code_hash(username, code_name)
    link = create_redirect_url(code_hash)
    qr_path = generate_qr_code(link)
    return code_hash, qr_path


def create_list_of_codes(request: HttpRequest) -> list[dict]:
    user = request.user
    qr_codes = QRCode.objects.filter(owner=user)
    params_to_dashboard = []
    for code in qr_codes:
        temporary = {
            "code_name": code.code_name,
            "direction": code.direction,
            "category": code.category if code.category else "Не задана",
            "end_time": code.end_time
            if code.category and code.end_time is not None
            else "бесконечности",
            "hash": code.code_hash,
            "image_path": settings.MEDIA_URL + code.path_to_file,
        }
        params_to_dashboard.append(temporary)
    return params_to_dashboard


def get_transitions_by_code(code: QRCode):
    return Transition.objects.filter(code=code)


def get_dataframe_by_code(code: QRCode) -> pd.DataFrame:
    transitions = get_transitions_by_code(code)

    if not transitions.exists():
        return pd.DataFrame(columns=["time_of_transition", "users"])

    list_of_times, list_of_users = zip(
        *transitions.values_list("created", "user_agent")
    )
    return pd.DataFrame({"time_of_transition": list_of_times, "users": list_of_users})


def prepare_data_to_plot(data: pd.DataFrame) -> pd.DataFrame:
    data["time_of_transition"] = pd.to_datetime(data["time_of_transition"])
    data["minute_of_transition"] = data["time_of_transition"].dt.round("min")
    for_plot = (
        data.groupby(by="minute_of_transition", as_index=False)
        .agg({"users": "count"})
        .sort_values(by="minute_of_transition")
    )
    return for_plot


def get_plot_html(data: pd.DataFrame):
    fig = px.scatter(
        data, x="minute_of_transition", y="users", title="Динамика переходов по QR коду"
    )
    plot_html = pio.to_html(fig, full_html=False)
    return plot_html


def create_plot_from_qr(code: QRCode):
    df = prepare_data_to_plot(get_dataframe_by_code(code))
    plot = get_plot_html(df)
    return plot
