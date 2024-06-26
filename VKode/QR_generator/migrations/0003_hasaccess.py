# Generated by Django 5.0.6 on 2024-05-26 15:06

import django.db.models.deletion
import utils.model_validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("QR_generator", "0002_transition_ip_address"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="HasAccess",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="UUID объекта",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        db_index=True,
                        default=utils.model_validators.get_current_time,
                        editable=False,
                        validators=[utils.model_validators.check_earlier_than_current],
                        verbose_name="Время создания объекта",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        default=utils.model_validators.get_current_time,
                        editable=False,
                        validators=[utils.model_validators.check_earlier_than_current],
                        verbose_name="Время изменения объекта",
                    ),
                ),
                (
                    "code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="QR_generator.qrcode",
                        verbose_name="QR код, к которому предоставляют доступ",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь, имеющий доступ к QR коду",
                    ),
                ),
            ],
            options={
                "verbose_name": "Доступ пользователя к QR коду",
                "verbose_name_plural": "Доступы пользователей к QR кодам",
                "db_table": "HasAccess",
            },
        ),
    ]
