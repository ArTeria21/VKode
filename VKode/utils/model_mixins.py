from django.db import models
from .model_validators import *
from uuid import uuid4


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
                                   validators=[check_earlier_than_current],
                                   db_index=True)

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
