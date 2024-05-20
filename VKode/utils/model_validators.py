from django.core.exceptions import ValidationError
from datetime import datetime, timezone


def get_current_time() -> datetime:
    """Функция возвращает текущее время в часовом поясе UTC"""
    return datetime.now(timezone.utc)


def check_earlier_than_current(dt: datetime) -> None:
    """Функция проверяет, является ли переданное время большим, чем текущее"""
    if dt > get_current_time():
        raise ValidationError('The set time is later than the current')


def check_later_than_current(dt: datetime) -> None:
    """Функция проверяет, является ли переданное время меньшим, чем текущее"""
    if dt < get_current_time():
        raise ValidationError('The set time is earlier than the current')
