from django.contrib import admin
from .models import Category, Client, QRCode

admin.site.register(Category)
admin.site.register(Client)
admin.site.register(QRCode)
