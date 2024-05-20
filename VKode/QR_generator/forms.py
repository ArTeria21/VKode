from django import forms

from django import forms
from .models import QRCode


class CreateQRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['code_name', 'direction', 'category', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
