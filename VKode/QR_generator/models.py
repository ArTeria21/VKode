from django.contrib.auth import get_user_model
from django.db import models
from utils.model_validators import check_later_than_current
from utils.model_mixins import UUIDMixin, CreatedMixin, ModifiedMixin


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


class QRCode(UUIDMixin, CreatedMixin, ModifiedMixin):
    """Модель, содержащая информацию о QR коде"""
    code_name = models.CharField(verbose_name='Название QR кода',
                                 max_length=255,
                                 null=False,
                                 blank=False)
    owner = models.ForeignKey(to=get_user_model(),
                              verbose_name='Создатель QR кода',
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    direction = models.URLField(verbose_name='URL адрес, куда ведёт QR код',
                                null=False,
                                blank=False)
    category = models.ForeignKey(to=Category,
                                 verbose_name='Категория QR кода',
                                 on_delete=models.SET_DEFAULT,
                                 null=True,
                                 blank=True,
                                 default='Категория не выбрана')
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
