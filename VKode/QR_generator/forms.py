from django import forms
from .models import QRCode, Category


class CreateQRCodeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = QRCode
        fields = ["code_name", "direction", "category", "end_time"]
        widgets = {
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
