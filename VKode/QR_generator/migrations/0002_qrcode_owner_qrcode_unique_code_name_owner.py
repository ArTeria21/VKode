# Generated by Django 5.0.6 on 2024-05-20 18:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QR_generator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='qrcode',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создатель QR кода'),
        ),
        migrations.AddConstraint(
            model_name='qrcode',
            constraint=models.UniqueConstraint(fields=('code_name', 'owner'), name='unique_code_name_owner'),
        ),
    ]
