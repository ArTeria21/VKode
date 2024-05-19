from django.db import models
from uuid import uuid4
from .model_validators import get_current_time, check_earlier_than_current, check_later_than_current
from django.conf.global_settings import AUTH_USER_MODEL


class UUIDMixin(models.Model):
    """Миксин, добавляющий поле ID, содержащее UUID объекта"""
    id = models.UUIDField(verbose_name='UUID объекта',
                          default=uuid4,
                          primary_key=True,
                          editable=False)

    class Meta:
        abstract = True


class CreatedMixin(models.Model):
    """Миксин, добавляющий поле Created, содержащее время создания объекта"""
    created = models.DateTimeField(verbose_name='Время создания объекта',
                                   default=get_current_time,
                                   editable=False,
                                   validators=[check_earlier_than_current])

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    """Миксин, добавляющий поле Modified, содержащее время последнего изменения объекта"""
    modified = models.DateTimeField(verbose_name='Время изменения объекта',
                                    default=get_current_time,
                                    editable=False,
                                    validators=[check_earlier_than_current])

    def save(self, *args, **kwargs):
        self.modified = get_current_time()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель, содержащая категории QR-кодов"""
    category = models.CharField(verbose_name='Название категории',
                                max_length=255,
                                null=False,
                                blank=False)

    def __str__(self) -> str:
        return f'<category: {self.category}>'

    class Meta:
        db_table = 'Categories'
        verbose_name = 'категория QR кода'
        verbose_name_plural = 'категории QR кодов'


class Client(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель, содержащая дополнительную информацию о пользователе"""
    user = models.OneToOneField(AUTH_USER_MODEL,
                                verbose_name='Аккаунт пользователя',
                                null=False,
                                blank=False,
                                unique=True,
                                on_delete=models.CASCADE)

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def email(self) -> str:
        return self.user.email

    def __str__(self) -> str:
        return f'<client:{self.username}>'

    class Meta:
        db_table = 'Clients'
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class QRCode(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель, содержащая информацию о QR коде"""
    code_name = models.CharField(verbose_name='Название QR кода',
                                 max_length=255,
                                 null=False,
                                 blank=False)
    owner = models.ForeignKey(to=Client,
                              verbose_name='Создатель QR кода',
                              on_delete=models.CASCADE,
                              null=False,
                              blank=False)
    direction = models.URLField(verbose_name='URL адрес, куда ведёт QR код',
                                null=False,
                                blank=False)
    category = models.ForeignKey(to=Category,
                                 verbose_name='Категория QR кода',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    end_time = models.DateTimeField(verbose_name='Время окончания работы QR кода',
                                    null=True,
                                    blank=True,
                                    validators=[check_later_than_current])
    path_to_file = models.FilePathField(verbose_name='Путь до QR Кода',
                                        editable=False,
                                        blank=False,
                                        null=False)

    def __str__(self) -> str:
        return f'<QR code: {self.code_name}>'

    class Meta:
        db_table = 'QR_codes'
        verbose_name = 'QR код'
        verbose_name_plural = 'QR коды'
        constraints = [
            models.UniqueConstraint(fields=['code_name', 'owner'], name='unique_code_name_owner')
        ]
